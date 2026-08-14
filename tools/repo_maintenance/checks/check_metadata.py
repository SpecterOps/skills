from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_json_text, load_yaml_text

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
TRUNCATED = re.compile(r"(?:\.\.\.|…)$")
SKILL_TOKEN = re.compile(r"\$[a-z0-9]+(?:-[a-z0-9]+)*")


def _frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    end = lines.index("---", 1)
    value = load_yaml_text("\n".join(lines[1:end]) + "\n")
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _local_path(
    diagnostics: list[Diagnostic], rule: str, owner: Path, root: Path, value: Any
) -> None:
    if not isinstance(value, str) or not value:
        return
    candidate = root / value
    if not _inside(root, candidate):
        diagnostics.append(
            Diagnostic(rule, owner.as_posix(), f"path escapes owning directory: {value}")
        )
    elif not candidate.exists():
        diagnostics.append(
            Diagnostic(rule, owner.as_posix(), f"local path does not exist: {value}")
        )


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skills: dict[str, Path] = {}
    for skill_root in sorted(context.root.glob("plugins/*/skills/*")):
        if not skill_root.is_dir():
            continue
        relative_root = skill_root.relative_to(context.root)
        skill_md = skill_root / "SKILL.md"
        ui_path = skill_root / "agents/openai.yaml"
        if not skill_md.is_file():
            diagnostics.append(
                Diagnostic(
                    "metadata.skill", relative_root.as_posix(), "skill directory lacks SKILL.md"
                )
            )
            continue
        try:
            frontmatter = _frontmatter(skill_md)
        except (OSError, ValueError) as exc:
            diagnostics.append(
                Diagnostic(
                    "metadata.skill", skill_md.relative_to(context.root).as_posix(), str(exc)
                )
            )
            continue
        name = frontmatter.get("name")
        if name != skill_root.name:
            diagnostics.append(
                Diagnostic(
                    "metadata.skill",
                    skill_md.relative_to(context.root).as_posix(),
                    f"frontmatter name must equal directory name {skill_root.name!r}",
                )
            )
        if isinstance(name, str):
            if name in skills:
                diagnostics.append(
                    Diagnostic(
                        "metadata.skill",
                        skill_md.relative_to(context.root).as_posix(),
                        "skill name duplicates "
                        f"{skills[name].relative_to(context.root).as_posix()}",
                    )
                )
            skills[name] = skill_md
        if not ui_path.is_file():
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui", relative_root.as_posix(), "skill lacks agents/openai.yaml"
                )
            )
            continue
        try:
            ui = load_yaml_text(ui_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui", ui_path.relative_to(context.root).as_posix(), str(exc)
                )
            )
            continue
        interface = ui.get("interface", {}) if isinstance(ui, dict) else {}
        description = interface.get("short_description")
        if not isinstance(description, str) or not 25 <= len(description) <= 64:
            length = len(description) if isinstance(description, str) else "non-string"
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui",
                    ui_path.relative_to(context.root).as_posix(),
                    f"short_description must be 25-64 characters (found {length})",
                )
            )
        elif TRUNCATED.search(description.rstrip()):
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui",
                    ui_path.relative_to(context.root).as_posix(),
                    "short_description must not end in a truncation suffix",
                )
            )
        prompt = interface.get("default_prompt")
        expected = f"${skill_root.name}"
        tokens = set(SKILL_TOKEN.findall(prompt)) if isinstance(prompt, str) else set()
        if expected not in tokens:
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui",
                    ui_path.relative_to(context.root).as_posix(),
                    f"default_prompt must contain exact token {expected}",
                )
            )
        color = interface.get("brand_color")
        if color is not None and (not isinstance(color, str) or not HEX_COLOR.fullmatch(color)):
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui",
                    ui_path.relative_to(context.root).as_posix(),
                    "brand_color must be a six-digit hex color",
                )
            )
        for key in ("icon_small", "icon_large"):
            _local_path(
                diagnostics,
                "metadata.skill-ui",
                ui_path.relative_to(context.root),
                skill_root,
                interface.get(key),
            )
        policy = ui.get("policy", {}) if isinstance(ui, dict) else {}
        for key, value in policy.items() if isinstance(policy, dict) else ():
            if not isinstance(value, bool):
                diagnostics.append(
                    Diagnostic(
                        "metadata.skill-ui",
                        ui_path.relative_to(context.root).as_posix(),
                        f"policy.{key} must be a boolean",
                    )
                )
        dependencies = ui.get("dependencies", {}) if isinstance(ui, dict) else {}
        tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []
        if not isinstance(tools, list):
            diagnostics.append(
                Diagnostic(
                    "metadata.skill-ui",
                    ui_path.relative_to(context.root).as_posix(),
                    "dependencies.tools must be a list",
                )
            )
        else:
            for index, tool in enumerate(tools):
                if (
                    not isinstance(tool, dict)
                    or tool.get("type") != "mcp"
                    or not isinstance(tool.get("value"), str)
                    or not tool["value"]
                ):
                    diagnostics.append(
                        Diagnostic(
                            "metadata.skill-ui",
                            ui_path.relative_to(context.root).as_posix(),
                            f"dependencies.tools[{index}] must be an MCP dependency with a value",
                        )
                    )

    for manifest_path in sorted(context.root.glob("plugins/*/.codex-plugin/plugin.json")):
        plugin_root = manifest_path.parents[1]
        try:
            manifest = load_json_text(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            diagnostics.append(
                Diagnostic(
                    "metadata.plugin", manifest_path.relative_to(context.root).as_posix(), str(exc)
                )
            )
            continue
        if not isinstance(manifest, dict):
            diagnostics.append(
                Diagnostic(
                    "metadata.plugin",
                    manifest_path.relative_to(context.root).as_posix(),
                    "plugin manifest must be a mapping",
                )
            )
            continue
        raw_interface = manifest.get("interface", {})
        interface = raw_interface if isinstance(raw_interface, dict) else {}
        prompts = interface.get("defaultPrompt", [])
        if isinstance(prompts, list) and len(prompts) > 3:
            diagnostics.append(
                Diagnostic(
                    "metadata.plugin",
                    manifest_path.relative_to(context.root).as_posix(),
                    f"interface.defaultPrompt has {len(prompts)} entries; maximum is 3",
                )
            )
        _local_path(
            diagnostics,
            "metadata.plugin",
            manifest_path.relative_to(context.root),
            plugin_root,
            manifest.get("skills"),
        )
        for key in ("composerIcon", "logo"):
            _local_path(
                diagnostics,
                "metadata.plugin",
                manifest_path.relative_to(context.root),
                plugin_root,
                interface.get(key),
            )

    skill_names = set(skills)
    for agent_path in sorted((context.root / "agents").glob("*.toml")):
        try:
            agent = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            diagnostics.append(
                Diagnostic(
                    "metadata.agent", agent_path.relative_to(context.root).as_posix(), str(exc)
                )
            )
            continue
        if agent.get("name") != agent_path.stem:
            diagnostics.append(
                Diagnostic(
                    "metadata.agent",
                    agent_path.relative_to(context.root).as_posix(),
                    f"declared name must equal filename {agent_path.stem!r}",
                )
            )
        instructions = agent.get("developer_instructions", "")
        if not isinstance(instructions, str):
            continue
        for token in sorted(set(SKILL_TOKEN.findall(instructions))):
            if token[1:] not in skill_names:
                diagnostics.append(
                    Diagnostic(
                        "metadata.agent",
                        agent_path.relative_to(context.root).as_posix(),
                        f"references unknown skill {token}",
                    )
                )
    return diagnostics


CHECK = CheckSpec(
    "metadata.consistency", frozenset({"metadata", "skills", "plugins", "agents"}), run
)
