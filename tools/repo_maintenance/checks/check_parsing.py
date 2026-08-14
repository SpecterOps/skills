from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

import yaml

from tools.repo_maintenance.files import relative_path, repository_files
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_json_text, load_yaml_text


def _diagnostic(
    root: Path, path: Path, reason: str, line: int | None = None, column: int | None = None
) -> Diagnostic:
    return Diagnostic("core.parse", relative_path(root, path), reason, line, column)


def _parse_frontmatter(root: Path, path: Path, text: str) -> list[Diagnostic]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return [_diagnostic(root, path, "SKILL.md must start with YAML frontmatter")]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return [_diagnostic(root, path, "SKILL.md frontmatter has no closing delimiter")]
    frontmatter = "\n".join(lines[1:end]) + "\n"
    try:
        value = load_yaml_text(frontmatter)
    except Exception as exc:
        return [_yaml_failure(root, path, exc, line_offset=1)]
    if not isinstance(value, dict):
        return [_diagnostic(root, path, "SKILL.md frontmatter must be a mapping")]
    return []


def _yaml_failure(root: Path, path: Path, exc: Exception, line_offset: int = 0) -> Diagnostic:
    if isinstance(exc, yaml.MarkedYAMLError) and exc.problem_mark is not None:
        mark = exc.problem_mark
        reason = exc.problem or str(exc).splitlines()[0]
        return _diagnostic(root, path, reason, mark.line + 1 + line_offset, mark.column + 1)
    return _diagnostic(root, path, str(exc))


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in repository_files(context.root):
        suffix = path.suffix.lower()
        if suffix not in {".json", ".yaml", ".yml", ".toml", ".py"} and path.name != "SKILL.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            diagnostics.append(_diagnostic(context.root, path, f"not valid UTF-8: {exc}"))
            continue
        try:
            if suffix == ".json":
                load_json_text(text)
            elif suffix in {".yaml", ".yml"}:
                load_yaml_text(text)
            elif suffix == ".toml":
                tomllib.loads(text)
            elif suffix == ".py":
                ast.parse(text, filename=relative_path(context.root, path), feature_version=(3, 13))
        except json.JSONDecodeError as exc:
            diagnostics.append(_diagnostic(context.root, path, exc.msg, exc.lineno, exc.colno))
        except tomllib.TOMLDecodeError as exc:
            diagnostics.append(_diagnostic(context.root, path, str(exc)))
        except SyntaxError as exc:
            diagnostics.append(_diagnostic(context.root, path, exc.msg, exc.lineno, exc.offset))
        except Exception as exc:
            diagnostics.append(_yaml_failure(context.root, path, exc))
        if path.name == "SKILL.md":
            diagnostics.extend(_parse_frontmatter(context.root, path, text))
    return diagnostics


CHECK = CheckSpec("core.parse", frozenset({"core", "parsing"}), run)
