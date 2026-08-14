from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.repo_maintenance.models import Diagnostic
from tools.repo_maintenance.schemas import load_json_text, load_schema, schema_errors

BEGIN = "<!-- BEGIN GENERATED PLUGIN CATALOG: run `just generate-catalog` -->"
END = "<!-- END GENERATED PLUGIN CATALOG -->"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
OUTPUTS = (
    Path(".agents/plugins/marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    Path("README.md"),
)


@dataclass(frozen=True)
class Plugin:
    name: str
    surfaces: tuple[str, ...]
    mcp: str
    status: str
    codex: dict[str, Any]
    claude: dict[str, Any] | None


def _diagnostic(path: str | Path, reason: str) -> Diagnostic:
    return Diagnostic("catalog.integrity", Path(path).as_posix(), reason)


def _read_json(path: Path) -> dict[str, Any]:
    value = load_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def _capabilities(plugin_root: Path) -> list[str]:
    result = [
        path.relative_to(plugin_root).as_posix() for path in plugin_root.glob("skills/*/SKILL.md")
    ]
    for directory in ("agents", "commands", "hooks", "mcp"):
        root = plugin_root / directory
        if root.is_dir():
            result.extend(
                path.relative_to(plugin_root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            )
    if (plugin_root / ".mcp.json").is_file():
        result.append(".mcp.json")
    return sorted(result)


def inspect(root: Path) -> tuple[list[Plugin], list[Diagnostic]]:
    config_path = root / "tools/maintenance/catalog.toml"
    diagnostics: list[Diagnostic] = []
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [], [_diagnostic(config_path.relative_to(root), str(exc))]
    for field, reason in schema_errors(config, load_schema(root, "catalog")):
        diagnostics.append(_diagnostic(config_path.relative_to(root), f"{field}: {reason}"))

    declarations = config.get("plugins", []) if isinstance(config, dict) else []
    names = [item.get("name") for item in declarations if isinstance(item, dict)]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    for name in duplicates:
        diagnostics.append(
            _diagnostic(config_path.relative_to(root), f"duplicate plugin order entry {name!r}")
        )
    plugin_dirs = sorted(path.name for path in (root / "plugins").iterdir() if path.is_dir())
    declared = {name for name in names if isinstance(name, str)}
    for name in sorted(set(plugin_dirs) - declared):
        diagnostics.append(_diagnostic(f"plugins/{name}", "plugin is missing from catalog.toml"))
    for name in sorted(declared - set(plugin_dirs)):
        diagnostics.append(
            _diagnostic(config_path.relative_to(root), f"declares missing plugin {name!r}")
        )

    agent_names = {path.stem for path in (root / "agents").glob("*.toml")}
    plugins: list[Plugin] = []
    for declaration in declarations:
        if not isinstance(declaration, dict) or not isinstance(declaration.get("name"), str):
            continue
        name = declaration["name"]
        plugin_root = root / "plugins" / name
        if not plugin_root.is_dir():
            continue
        ownership_path = plugin_root / "ownership.json"
        codex_path = plugin_root / ".codex-plugin/plugin.json"
        try:
            ownership = _read_json(ownership_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            diagnostics.append(_diagnostic(ownership_path.relative_to(root), str(exc)))
            continue
        for field, reason in schema_errors(ownership, load_schema(root, "ownership")):
            diagnostics.append(_diagnostic(ownership_path.relative_to(root), f"{field}: {reason}"))
        if ownership.get("plugin") != name:
            diagnostics.append(
                _diagnostic(ownership_path.relative_to(root), f"plugin must equal {name!r}")
            )

        surfaces = tuple(declaration.get("surfaces", ()))
        manifests: dict[str, dict[str, Any] | None] = {"codex": None, "claude": None}
        for surface, relative in (
            ("codex", Path(".codex-plugin/plugin.json")),
            ("claude", Path(".claude-plugin/plugin.json")),
        ):
            path = plugin_root / relative
            if surface in surfaces and not path.is_file():
                diagnostics.append(
                    _diagnostic(path.relative_to(root), f"required {surface} manifest is missing")
                )
                continue
            if path.is_file():
                try:
                    manifests[surface] = _read_json(path)
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    diagnostics.append(_diagnostic(path.relative_to(root), str(exc)))
                else:
                    assert manifests[surface] is not None
                    for field, reason in schema_errors(
                        manifests[surface], load_schema(root, f"{surface}-plugin")
                    ):
                        diagnostics.append(
                            _diagnostic(path.relative_to(root), f"{field}: {reason}")
                        )
        codex = manifests["codex"]
        if not isinstance(codex, dict):
            diagnostics.append(
                _diagnostic(
                    codex_path.relative_to(root), "Codex manifest is required as canonical metadata"
                )
            )
            continue
        for key in ("name", "version", "description"):
            if key == "name" and codex.get(key) != name:
                diagnostics.append(
                    _diagnostic(codex_path.relative_to(root), f"name must equal {name!r}")
                )
        version = codex.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            diagnostics.append(
                _diagnostic(codex_path.relative_to(root), f"invalid semantic version {version!r}")
            )
        claude = manifests["claude"]
        if isinstance(claude, dict):
            for key in ("name", "version", "description"):
                if claude.get(key) != codex.get(key):
                    diagnostics.append(
                        _diagnostic(
                            plugin_root.relative_to(root),
                            f"Codex and Claude manifest field {key!r} must match",
                        )
                    )

        discovered_skills = sorted(
            path.parent.name for path in plugin_root.glob("skills/*/SKILL.md")
        )
        owned_skills = ownership.get("skills")
        if isinstance(owned_skills, list) and sorted(owned_skills) != discovered_skills:
            diagnostics.append(
                _diagnostic(
                    ownership_path.relative_to(root),
                    f"skills must exactly match packaged skills: {discovered_skills!r}",
                )
            )
        for agent in ownership.get("agents", []):
            if isinstance(agent, str) and agent not in agent_names:
                diagnostics.append(
                    _diagnostic(ownership_path.relative_to(root), f"unknown agent {agent!r}")
                )

        status = ownership.get("status")
        capabilities = _capabilities(plugin_root)
        if status == "active" and not capabilities:
            diagnostics.append(
                _diagnostic(
                    plugin_root.relative_to(root), "active plugin has no packaged capability"
                )
            )
        if status == "incubating":
            if capabilities:
                diagnostics.append(
                    _diagnostic(
                        plugin_root.relative_to(root),
                        "incubating plugin has a packaged capability; promotion requires an "
                        "explicit status change",
                    )
                )
            if "claude" in surfaces:
                diagnostics.append(
                    _diagnostic(
                        config_path.relative_to(root),
                        f"incubating plugin {name!r} cannot be published to Claude",
                    )
                )
            prompts = codex.get("interface", {}).get("defaultPrompt", [])
            if prompts:
                diagnostics.append(
                    _diagnostic(
                        codex_path.relative_to(root),
                        "incubating plugin must not advertise default prompts",
                    )
                )

        plugins.append(
            Plugin(
                name=name,
                surfaces=surfaces,
                mcp=declaration.get("mcp", "-"),
                status=str(status),
                codex=codex,
                claude=claude if isinstance(claude, dict) else None,
            )
        )
    return plugins, diagnostics


def _readme(root: Path, plugins: list[Plugin]) -> str:
    path = root / "README.md"
    current = path.read_text(encoding="utf-8")
    if current.count(BEGIN) != 1 or current.count(END) != 1:
        raise ValueError(f"README.md must contain exactly one {BEGIN!r} and {END!r} marker")
    start = current.index(BEGIN)
    finish = current.index(END, start) + len(END)
    lines = [
        BEGIN,
        "",
        "| Plugin | Codex | Claude Code | MCP | Description |",
        "|---|---:|---:|---:|---|",
    ]
    for plugin in plugins:
        codex = (
            "Planned"
            if plugin.status == "incubating"
            else ("Yes" if "codex" in plugin.surfaces else "-")
        )
        claude = "Yes" if plugin.status == "active" and "claude" in plugin.surfaces else "-"
        description = str(plugin.codex["description"]).replace("|", "\\|")
        if plugin.status == "incubating":
            description += " Planned; no capability is currently packaged."
        lines.append(
            f"| [{plugin.name}](plugins/{plugin.name}/README.md) | {codex} | {claude} | "
            f"{plugin.mcp} | {description} |"
        )
    lines.extend(("", END))
    return current[:start] + "\n".join(lines) + current[finish:]


def expected_outputs(root: Path) -> tuple[dict[Path, str], list[Diagnostic]]:
    plugins, diagnostics = inspect(root)
    if diagnostics:
        return {}, diagnostics
    codex_plugins = []
    claude_plugins = []
    for plugin in plugins:
        if "codex" in plugin.surfaces:
            codex_plugins.append(
                {
                    "name": plugin.name,
                    "source": {"source": "local", "path": f"./plugins/{plugin.name}"},
                    "policy": {
                        "installation": "AVAILABLE"
                        if plugin.status == "active"
                        else "NOT_AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": plugin.codex["interface"]["category"],
                }
            )
        if plugin.status == "active" and "claude" in plugin.surfaces:
            assert plugin.claude is not None
            claude_plugins.append(
                {
                    "name": plugin.name,
                    "source": f"./plugins/{plugin.name}",
                    "description": plugin.claude["description"],
                    "version": plugin.claude["version"],
                    "category": str(plugin.codex["interface"]["category"]).lower(),
                }
            )
    try:
        readme = _readme(root, plugins)
    except (OSError, ValueError) as exc:
        return {}, [_diagnostic("README.md", str(exc))]
    outputs = {
        OUTPUTS[0]: json.dumps(
            {
                "name": "specterops-skills",
                "interface": {"displayName": "SpecterOps Skills"},
                "plugins": codex_plugins,
            },
            indent=2,
        )
        + "\n",
        OUTPUTS[1]: json.dumps(
            {
                "name": "specterops-skills",
                "owner": {"name": "SpecterOps"},
                "metadata": {
                    "description": (
                        "SpecterOps skills, plugins, and agents for offensive security "
                        "and engineering workflows"
                    ),
                    "pluginRoot": "./plugins",
                },
                "plugins": claude_plugins,
            },
            indent=2,
        )
        + "\n",
        OUTPUTS[2]: readme,
    }
    return outputs, []


def check(root: Path) -> list[Diagnostic]:
    outputs, diagnostics = expected_outputs(root)
    if diagnostics:
        return diagnostics
    for relative, expected in outputs.items():
        path = root / relative
        try:
            actual = path.read_text(encoding="utf-8")
        except OSError as exc:
            diagnostics.append(_diagnostic(relative, str(exc)))
            continue
        if actual != expected:
            diagnostics.append(
                _diagnostic(relative, "generated catalog is stale; run `just generate-catalog`")
            )
    return diagnostics


def generate(root: Path) -> None:
    outputs, diagnostics = expected_outputs(root)
    if diagnostics:
        raise RuntimeError("\n".join(item.render() for item in diagnostics))
    originals: dict[Path, tuple[bytes | None, int]] = {}
    for relative in outputs:
        destination = root / relative
        if destination.is_file():
            originals[relative] = (
                destination.read_bytes(),
                stat.S_IMODE(destination.stat().st_mode),
            )
        else:
            originals[relative] = (None, 0o644)
    installed: list[Path] = []
    ready_paths: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="skills-catalog-") as temporary:
        stage = Path(temporary)
        for relative, contents in outputs.items():
            staged = stage / relative
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_text(contents, encoding="utf-8")
        try:
            for relative in outputs:
                destination = root / relative
                with tempfile.NamedTemporaryFile(
                    dir=destination.parent, prefix=f".{destination.name}.", delete=False
                ) as handle:
                    ready = Path(handle.name)
                ready_paths.append(ready)
                shutil.copyfile(stage / relative, ready)
                ready.chmod(originals[relative][1])
                os.replace(ready, destination)
                ready_paths.remove(ready)
                installed.append(relative)
        except OSError:
            for relative in installed:
                destination = root / relative
                contents, mode = originals[relative]
                if contents is None:
                    destination.unlink(missing_ok=True)
                    continue
                with tempfile.NamedTemporaryFile(
                    dir=destination.parent, prefix=f".{destination.name}.restore.", delete=False
                ) as handle:
                    restore = Path(handle.name)
                    handle.write(contents)
                restore.chmod(mode)
                os.replace(restore, destination)
            raise
        finally:
            for ready in ready_paths:
                ready.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or check repository plugin catalogs")
    parser.add_argument("command", choices=("generate", "check"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    arguments = parser.parse_args(argv)
    if arguments.command == "generate":
        try:
            generate(arguments.root.resolve())
        except (OSError, RuntimeError, ValueError) as exc:
            parser.error(str(exc))
        return 0
    diagnostics = check(arguments.root.resolve())
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
