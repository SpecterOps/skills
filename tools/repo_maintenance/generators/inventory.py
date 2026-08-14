from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

from tools.repo_maintenance.models import Diagnostic
from tools.repo_maintenance.transaction import install_text_outputs

SKILLS_BEGIN = "<!-- BEGIN GENERATED SKILL INVENTORY: run `just generate-inventory` -->"
SKILLS_END = "<!-- END GENERATED SKILL INVENTORY -->"
AGENTS_BEGIN = "<!-- BEGIN GENERATED AGENT INVENTORY: run `just generate-inventory` -->"
AGENTS_END = "<!-- END GENERATED AGENT INVENTORY -->"
MCP_BEGIN = "<!-- BEGIN GENERATED MCP INVENTORY: run `just generate-inventory` -->"
MCP_END = "<!-- END GENERATED MCP INVENTORY -->"


def _diagnostic(reason: str) -> Diagnostic:
    return Diagnostic("inventory.generated", "README.md", reason)


def _replace(text: str, begin: str, end: str, lines: list[str]) -> str:
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"README.md must contain exactly one {begin!r} and {end!r} marker")
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    return text[:start] + "\n".join((begin, "", *lines, "", end)) + text[finish:]


def _plugin_order(root: Path) -> dict[str, int]:
    config = tomllib.loads((root / "tools/maintenance/catalog.toml").read_text(encoding="utf-8"))
    return {item["name"]: index for index, item in enumerate(config.get("plugins", []))}


def _skill_lines(root: Path) -> list[str]:
    order = _plugin_order(root)
    skills = []
    for path in root.glob("plugins/*/skills/*/SKILL.md"):
        plugin = path.parents[2].name
        skill = path.parent.name
        skills.append((order.get(plugin, len(order)), plugin, skill, path.relative_to(root)))
    skills.sort(key=lambda item: (item[0], item[1], item[2]))
    lines = ["| Skill | Plugin | Path |", "|---|---|---|"]
    lines.extend(
        f"| `{skill}` | `{plugin}` | [SKILL.md]({relative.as_posix()}) |"
        for _, plugin, skill, relative in skills
    )
    return lines


def _agent_lines(root: Path) -> list[str]:
    lines = ["| Agent | Path |", "|---|---|"]
    for path in sorted((root / "agents").glob("*.toml")):
        relative = path.relative_to(root).as_posix()
        lines.append(f"| `{path.stem}` | [{relative}]({relative}) |")
    return lines


def _mcp_lines(root: Path) -> list[str]:
    config = tomllib.loads((root / "tools/maintenance/inventory.toml").read_text(encoding="utf-8"))
    entries = config.get("mcp", [])
    lines = ["| MCP Server | Plugin | Configuration |", "|---|---|---|"]
    lines.extend(
        f"| `{item['server']}` | `{item['plugin']}` | {item['configuration']} |" for item in entries
    )
    return lines


def expected(root: Path) -> tuple[str | None, list[Diagnostic]]:
    try:
        text = (root / "README.md").read_text(encoding="utf-8")
        for begin, end in (
            (SKILLS_BEGIN, SKILLS_END),
            (AGENTS_BEGIN, AGENTS_END),
            (MCP_BEGIN, MCP_END),
        ):
            if text.count(begin) != 1 or text.count(end) != 1:
                raise ValueError(f"README.md must contain exactly one {begin!r} and {end!r} marker")
        text = _replace(text, SKILLS_BEGIN, SKILLS_END, _skill_lines(root))
        text = _replace(text, AGENTS_BEGIN, AGENTS_END, _agent_lines(root))
        text = _replace(text, MCP_BEGIN, MCP_END, _mcp_lines(root))
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        return None, [_diagnostic(str(exc))]
    return text, []


def check(root: Path) -> list[Diagnostic]:
    expected_text, diagnostics = expected(root)
    if diagnostics:
        return diagnostics
    assert expected_text is not None
    if (root / "README.md").read_text(encoding="utf-8") != expected_text:
        return [_diagnostic("generated inventory is stale; run `just generate-inventory`")]
    return []


def generate(root: Path) -> None:
    text, diagnostics = expected(root)
    if diagnostics:
        raise RuntimeError("\n".join(item.render() for item in diagnostics))
    assert text is not None
    install_text_outputs(root, {Path("README.md"): text})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or check root repository inventories")
    parser.add_argument("command", choices=("generate", "check"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if arguments.command == "generate":
        try:
            generate(root)
        except (OSError, RuntimeError, ValueError) as exc:
            parser.error(str(exc))
        return 0
    diagnostics = check(root)
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
