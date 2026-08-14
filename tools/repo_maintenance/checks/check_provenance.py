from __future__ import annotations

import hashlib
import subprocess
import tomllib
from pathlib import Path

from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_schema, schema_errors

MUTABLE_REFS = {"head", "main", "master", "latest", "trunk", "develop", "development"}


def _tracked_artifacts(root: Path) -> set[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--", "plugins"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode(errors="replace").strip())
    result = set()
    for raw in completed.stdout.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8")
        if Path(relative).suffix.lower() in {".dll", ".exe"}:
            result.add(relative)
    return result


def run(context: CheckContext) -> list[Diagnostic]:
    config_path = context.root / "tools/maintenance/provenance.toml"
    diagnostics: list[Diagnostic] = []
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [Diagnostic("provenance.inventory", "tools/maintenance/provenance.toml", str(exc))]
    for field, reason in schema_errors(config, load_schema(context.root, "provenance")):
        diagnostics.append(
            Diagnostic(
                "provenance.inventory", "tools/maintenance/provenance.toml", f"{field}: {reason}"
            )
        )
    entries = config.get("artifacts", []) if isinstance(config, dict) else []
    paths = [item.get("path") for item in entries if isinstance(item, dict)]
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    for path in duplicates:
        diagnostics.append(
            Diagnostic(
                "provenance.inventory",
                "tools/maintenance/provenance.toml",
                f"duplicate artifact path {path!r}",
            )
        )
    try:
        tracked = _tracked_artifacts(context.root)
    except RuntimeError as exc:
        return [Diagnostic("provenance.inventory", ".", f"cannot inspect Git index: {exc}")]
    declared = {path for path in paths if isinstance(path, str)}
    for path in sorted(tracked - declared):
        diagnostics.append(
            Diagnostic("provenance.inventory", path, "tracked PE artifact lacks provenance")
        )
    for path in sorted(declared - tracked):
        diagnostics.append(
            Diagnostic(
                "provenance.inventory",
                path,
                "provenance entry is stale or not a tracked PE artifact",
            )
        )
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        relative = entry["path"]
        candidate = (context.root / relative).resolve()
        try:
            candidate.relative_to(context.root.resolve())
        except ValueError:
            diagnostics.append(
                Diagnostic("provenance.inventory", relative, "path escapes repository root")
            )
            continue
        immutable_ref = entry.get("immutable_ref")
        if isinstance(immutable_ref, str) and immutable_ref.lower() in MUTABLE_REFS:
            diagnostics.append(
                Diagnostic(
                    "provenance.inventory", relative, f"mutable source ref {immutable_ref!r}"
                )
            )
        if relative in tracked and not candidate.is_file():
            diagnostics.append(
                Diagnostic(
                    "provenance.inventory",
                    relative,
                    "tracked artifact is missing or not a file in the worktree",
                )
            )
            continue
        if candidate.is_file() and isinstance(entry.get("sha256"), str):
            actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if actual != entry["sha256"]:
                diagnostics.append(
                    Diagnostic(
                        "provenance.inventory",
                        relative,
                        f"SHA-256 mismatch: expected {entry['sha256']}, found {actual}",
                    )
                )
    return diagnostics


CHECK = CheckSpec("provenance.inventory", frozenset({"provenance", "portability"}), run)
