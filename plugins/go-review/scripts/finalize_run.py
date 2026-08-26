#!/usr/bin/env python3
"""Reconcile go-review finding shards and initialize deterministic reports."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def resolve_finding_path(path: Path, findings_root: Path) -> tuple[Path | None, str | None]:
    """Resolve and validate a finding path before adding it to the report index."""
    candidate = path.resolve()
    if candidate.parent != findings_root:
        return None, "out-of-bounds"
    if candidate.suffix != ".md":
        return None, "non-Markdown"
    if not candidate.is_file():
        return None, "missing"
    return candidate, None


def reconcile(output_dir: Path) -> tuple[list[Path], list[str]]:
    findings_dir = output_dir / "findings"
    findings_root = findings_dir.resolve()
    indexed: set[Path] = set()
    warnings: list[str] = []
    plan = json.loads((output_dir / "plan.json").read_text(encoding="utf-8"))
    for worker in plan.get("workers", []):
        worker_id = f"worker-{worker['worker_n']}"
        shard = output_dir / "findings-index.d" / f"{worker_id}.txt"
        if not shard.is_file():
            warnings.append(f"- {worker_id}: missing finding shard")
            continue
        for raw in shard.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                candidate = Path(raw.strip())
                if not candidate.is_absolute():
                    candidate = output_dir / candidate
                resolved, reason = resolve_finding_path(candidate, findings_root)
                if resolved is None:
                    warnings.append(f"- {worker_id}: ignored {reason} shard path: {candidate.resolve()}")
                    continue
                indexed.add(resolved)
    disk_findings: set[Path] = set()
    for path in findings_dir.glob("*.md"):
        resolved, reason = resolve_finding_path(path, findings_root)
        if resolved is None:
            warnings.append(f"- ignored {reason} orphan finding path: {path.resolve()}")
            continue
        disk_findings.add(resolved)
    for orphan in sorted(disk_findings - indexed):
        warnings.append(f"- orphan finding retained: {orphan}")
    findings = sorted(indexed | disk_findings)
    (output_dir / "findings-index.txt").write_text(
        "".join(f"{path}\n" for path in findings), encoding="utf-8"
    )
    summary = ["# Run Summary", "", f"Findings reconciled: {len(findings)}", ""]
    if not plan.get("workers"):
        summary.extend(["No capability-gated review clusters were selected.", ""])
    if warnings:
        summary.extend(["## Warnings", "", *warnings, ""])
    (output_dir / "run-summary.md").write_text("\n".join(summary), encoding="utf-8")
    return findings, warnings


def initialize_empty_reports(output_dir: Path) -> None:
    (output_dir / "dedup-summary.md").write_text(
        "# Deduplication Summary\n\nNo findings to deduplicate.\n", encoding="utf-8"
    )
    (output_dir / "fp-summary.md").write_text(
        "# False-Positive and Severity Summary\n\nNo findings to judge.\n", encoding="utf-8"
    )
    (output_dir / "REPORT.md").write_text(
        "# Go Security Review\n\nNo reportable findings.\n", encoding="utf-8"
    )
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("generate_sarif.py")), str(output_dir)],
        check=True,
        capture_output=True,
        text=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    findings, _ = reconcile(args.output_dir.resolve())
    if not findings:
        initialize_empty_reports(args.output_dir.resolve())
    print(json.dumps({"finding_count": len(findings)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
