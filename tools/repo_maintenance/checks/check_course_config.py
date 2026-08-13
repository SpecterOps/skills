from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance.files import relative_path
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_schema, load_yaml_text, schema_errors

CONFIG_DIR = Path(
    "plugins/internal-training-course/skills/course-wiki-migration-orchestrator/references"
)
CONFIG_NAMES = ("atrto-config.yaml", "course-config-template.yaml")


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    schema = load_schema(context.root, "course-config")
    for name in CONFIG_NAMES:
        path = context.root / CONFIG_DIR / name
        try:
            value = load_yaml_text(path.read_text(encoding="utf-8"))
        except Exception as exc:
            diagnostics.append(
                Diagnostic("course-config.schema", relative_path(context.root, path), str(exc))
            )
            continue
        for field, reason in schema_errors(value, schema):
            diagnostics.append(
                Diagnostic(
                    "course-config.schema",
                    relative_path(context.root, path),
                    f"{field}: {reason}",
                )
            )
    return diagnostics


CHECK = CheckSpec("course-config.schema", frozenset({"course-config"}), run)
