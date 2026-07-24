#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validate worker shards and coverage files against plan.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from generate_sarif import split_frontmatter


FINDING_ID_RE = re.compile(r"\b[A-Z][A-Z0-9_]*-\d{3,}\b")


def frontmatter_id(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(text)
    value = frontmatter.get("id")
    return None if value is None else str(value)


def normalize_worker_id(value: str) -> str:
    suffix = value.removeprefix("worker-") if value.startswith("worker-") else value
    if not suffix.isdigit():
        raise ValueError(f"invalid worker id: {value!r}")
    return f"worker-{int(suffix)}"


def flatten_claimed_count_args(values: list[list[str]]) -> list[str]:
    return [value for group in values for value in group]


def parse_claimed_counts(values: list[str]) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for value in values:
        worker, sep, count = value.partition("=")
        if not sep:
            raise ValueError(f"invalid --claimed-count {value!r}; expected worker-N=N")
        worker_id = normalize_worker_id(worker)
        try:
            number = int(count)
        except ValueError as exc:
            raise ValueError(f"invalid claimed count for {worker_id}: {count!r}") from exc
        if number < 0:
            raise ValueError(f"invalid claimed count for {worker_id}: {number}")
        parsed[worker_id] = number
    return parsed


def _output_dir(plan: dict[str, Any], plan_path: Path) -> Path:
    configured = plan.get("run", {}).get("output_dir")
    return Path(configured) if configured else plan_path.parent


def _worker_map(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    workers: dict[str, dict[str, Any]] = {}
    for worker in plan.get("workers", []):
        if "worker_n" not in worker:
            raise ValueError(f"plan worker entry missing 'worker_n': {worker!r}")
        workers[normalize_worker_id(str(worker["worker_n"]))] = worker
    return workers


def _read_shard(path: Path, output_dir: Path) -> tuple[list[Path], dict[str, Path]]:
    paths: list[Path] = []
    ids: dict[str, Path] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = output_dir / candidate
        paths.append(candidate)
        ids[candidate.stem] = candidate
    return paths, ids


def _is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _parse_coverage_rows(path: Path) -> tuple[dict[tuple[str, str], str], list[str]]:
    rows: dict[tuple[str, str], str] = {}
    errors: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0].lower() == "pass prefix" or _is_separator(cells):
            continue
        key = (cells[0], cells[1])
        if key in rows:
            errors.append(
                f"{path}: duplicate coverage row for {cells[0]} / {cells[1]} "
                f"at line {line_no}"
            )
        rows[key] = cells[2]
    return rows, errors


def _valid_cleared(outcome: str) -> bool:
    lowered = outcome.lower()
    return lowered == "cleared" or lowered.startswith("cleared ") or lowered.startswith("cleared(")


def _validate_worker(
    worker_id: str,
    worker: dict[str, Any],
    *,
    output_dir: Path,
    claimed_counts: dict[str, int],
) -> list[str]:
    errors: list[str] = []
    worker_n = int(worker_id.removeprefix("worker-"))
    shard_path = output_dir / "findings-index.d" / f"worker-{worker_n}.txt"
    coverage_path = output_dir / "coverage" / f"worker-{worker_n}.md"
    shard_paths: list[Path] = []
    shard_ids: dict[str, Path] = {}
    if not shard_path.is_file():
        errors.append(f"{worker_id}: missing shard {shard_path}")
    else:
        shard_paths, shard_ids = _read_shard(shard_path, output_dir)
        if len(shard_paths) != len(shard_ids):
            errors.append(f"{worker_id}: shard contains duplicate finding IDs")
        findings_dir = (output_dir / "findings").resolve()
        for path in shard_paths:
            if not path.is_file():
                errors.append(f"{worker_id}: shard references missing finding file {path}")
                continue
            if path.resolve().parent != findings_dir:
                errors.append(f"{worker_id}: shard references finding outside findings/: {path}")
            try:
                declared = frontmatter_id(path)
            except Exception as exc:
                errors.append(f"{worker_id}: finding {path.name} has invalid frontmatter: {exc}")
                continue
            if declared is None:
                errors.append(f"{worker_id}: finding {path.name} has no parseable frontmatter id")
            elif declared != path.stem:
                errors.append(
                    f"{worker_id}: finding {path.name} frontmatter id {declared!r} "
                    f"does not match its filename stem {path.stem!r}"
                )
    if worker_id in claimed_counts and claimed_counts[worker_id] != len(shard_paths):
        errors.append(
            f"{worker_id}: claimed {claimed_counts[worker_id]} finding files but shard has "
            f"{len(shard_paths)} entries"
        )
    if not coverage_path.is_file():
        errors.append(f"{worker_id}: missing coverage file {coverage_path}")
        return errors
    rows, coverage_errors = _parse_coverage_rows(coverage_path)
    errors.extend(f"{worker_id}: {error}" for error in coverage_errors)
    declared_ids: set[str] = set()
    for prefix, bug_class in zip(
        worker.get("pass_prefixes", []),
        worker.get("pass_bug_classes", []),
        strict=True,
    ):
        outcome = rows.get((prefix, bug_class))
        if outcome is None:
            errors.append(f"{worker_id}: missing coverage row for {prefix} / {bug_class}")
            continue
        if outcome.lower().startswith("filed:"):
            ids = FINDING_ID_RE.findall(outcome)
            if not ids:
                errors.append(f"{worker_id}: filed outcome for {prefix} has no finding IDs")
            for finding_id in ids:
                declared_ids.add(finding_id)
                if not finding_id.startswith(f"{prefix}-"):
                    errors.append(
                        f"{worker_id}: filed ID {finding_id} does not match pass prefix {prefix}"
                    )
                if finding_id not in shard_ids:
                    errors.append(f"{worker_id}: filed ID {finding_id} is absent from shard")
        elif not _valid_cleared(outcome):
            errors.append(f"{worker_id}: invalid coverage outcome for {prefix}: {outcome}")
    for finding_id in sorted(set(shard_ids) - declared_ids):
        errors.append(f"{worker_id}: shard ID {finding_id} is not declared in coverage")
    return errors


def validate_plan(
    plan_path: Path,
    *,
    workers: list[str] | None = None,
    claimed_counts: dict[str, int] | None = None,
) -> list[str]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    output_dir = _output_dir(plan, plan_path)
    worker_map = _worker_map(plan)
    selected = (
        sorted(worker_map)
        if workers is None
        else [normalize_worker_id(worker) for worker in workers]
    )
    errors: list[str] = []
    for worker_id in selected:
        worker = worker_map.get(worker_id)
        if worker is None:
            errors.append(f"{worker_id}: not present in {plan_path}")
            continue
        errors.extend(
            _validate_worker(
                worker_id,
                worker,
                output_dir=output_dir,
                claimed_counts=claimed_counts or {},
            )
        )
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan_json", type=Path)
    parser.add_argument("--worker", action="append")
    parser.add_argument("--claimed-count", action="append", nargs="+", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        errors = validate_plan(
            args.plan_json,
            workers=args.worker,
            claimed_counts=parse_claimed_counts(flatten_claimed_count_args(args.claimed_count)),
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"validate_artifacts: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("validate_artifacts: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
