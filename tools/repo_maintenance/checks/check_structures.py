from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

import yaml

from tools.repo_maintenance.files import relative_path
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import (
    load_json_text,
    load_schema,
    load_yaml_text,
    schema_errors,
)


def _inputs(root: Path) -> list[tuple[Path, str, str]]:
    result: list[tuple[Path, str, str]] = []
    result.extend(
        (path, "codex-plugin", "json") for path in root.glob("plugins/*/.codex-plugin/plugin.json")
    )
    result.extend(
        (path, "claude-plugin", "json")
        for path in root.glob("plugins/*/.claude-plugin/plugin.json")
    )
    result.extend((path, "ownership", "json") for path in root.glob("plugins/*/ownership.json"))
    result.extend(
        (path, "skill-ui", "yaml") for path in root.glob("plugins/*/skills/*/agents/openai.yaml")
    )
    result.extend(
        (path, "skill-frontmatter", "frontmatter")
        for path in root.glob("plugins/*/skills/*/SKILL.md")
    )
    result.extend((path, "root-agent", "toml") for path in root.glob("agents/*.toml"))
    result.append((root / ".agents/plugins/marketplace.json", "codex-marketplace", "json"))
    result.append((root / ".claude-plugin/marketplace.json", "claude-marketplace", "json"))
    return sorted(result, key=lambda item: item[0].relative_to(root).as_posix())


def _load(path: Path, kind: str) -> Any:
    text = path.read_text(encoding="utf-8")
    if kind == "json":
        return load_json_text(text)
    if kind == "yaml":
        return load_yaml_text(text)
    if kind == "frontmatter":
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            raise ValueError("SKILL.md must start with YAML frontmatter")
        try:
            end = lines.index("---", 1)
        except ValueError as exc:
            raise ValueError("SKILL.md frontmatter has no closing delimiter") from exc
        return load_yaml_text("\n".join(lines[1:end]) + "\n")
    return tomllib.loads(text)


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path, schema_name, kind in _inputs(context.root):
        try:
            value = _load(path, kind)
            schema = load_schema(context.root, schema_name)
        except (
            OSError,
            ValueError,
            TypeError,
            json.JSONDecodeError,
            tomllib.TOMLDecodeError,
            yaml.YAMLError,
        ) as exc:
            diagnostics.append(
                Diagnostic("core.structure", relative_path(context.root, path), str(exc))
            )
            continue
        for field, reason in schema_errors(value, schema):
            diagnostics.append(
                Diagnostic(
                    "core.structure",
                    relative_path(context.root, path),
                    f"{field}: {reason}",
                )
            )
    return diagnostics


CHECK = CheckSpec(
    "core.structure",
    frozenset({"core", "plugins", "skills", "ownership", "agents", "catalogs"}),
    run,
)
