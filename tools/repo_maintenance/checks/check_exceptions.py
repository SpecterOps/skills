from __future__ import annotations

import datetime as dt
import tomllib
from pathlib import Path

from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic

REQUIRED = {"rule", "path", "rationale", "owner", "expires"}
GLOB_MARKERS = frozenset("*?[]{}")


def validate(value: object, *, today: dt.date | None = None) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    entries = value.get("exceptions") if isinstance(value, dict) else None
    if not isinstance(entries, list):
        return [
            Diagnostic(
                "exceptions.policy",
                "tools/maintenance/exceptions.toml",
                "exceptions must be an array",
            )
        ]
    current = today or dt.date.today()
    for index, entry in enumerate(entries):
        prefix = f"exceptions[{index}]"

        def issue(reason: str) -> None:
            diagnostics.append(
                Diagnostic("exceptions.policy", "tools/maintenance/exceptions.toml", reason)
            )

        if not isinstance(entry, dict):
            issue(f"{prefix} must be a table")
            continue
        fields = set(entry)
        if fields != REQUIRED:
            missing = sorted(REQUIRED - fields)
            extra = sorted(fields - REQUIRED)
            details = []
            if missing:
                details.append("missing " + ", ".join(missing))
            if extra:
                details.append("unknown " + ", ".join(extra))
            issue(f"{prefix} has invalid fields: {'; '.join(details)}")
        for field in ("rule", "path", "rationale", "owner"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                issue(f"{prefix}.{field} must be a non-empty string")
        path = entry.get("path")
        if isinstance(path, str) and (
            Path(path).is_absolute()
            or ".." in Path(path).parts
            or any(c in path for c in GLOB_MARKERS)
        ):
            issue(f"{prefix}.path must be an exact repository-relative path without globs")
        expires = entry.get("expires")
        if not isinstance(expires, dt.date):
            issue(f"{prefix}.expires must be an ISO date")
        elif expires < current:
            issue(f"{prefix} expired on {expires.isoformat()}")
    return diagnostics


def run(context: CheckContext) -> list[Diagnostic]:
    relative = Path("tools/maintenance/exceptions.toml")
    try:
        value = tomllib.loads((context.root / relative).read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [Diagnostic("exceptions.policy", relative.as_posix(), str(exc))]
    return validate(value)


CHECK = CheckSpec("exceptions.policy", frozenset({"exceptions", "policy"}), run)
