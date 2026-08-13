from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from tools.repo_maintenance.discovery import DiscoveryError, discover_checks
from tools.repo_maintenance.models import CheckContext


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], check=False, capture_output=True, text=True
    )
    if result.returncode:
        raise RuntimeError("repository maintenance must run inside a Git worktree")
    return Path(result.stdout.strip()).resolve()


def _normalize_target(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def validate(target: str) -> int:
    try:
        checks = discover_checks()
    except DiscoveryError as exc:
        print(f"maintenance.discovery: {exc}", file=sys.stderr)
        return 1
    normalized = _normalize_target(target)
    known_targets = sorted({item for check in checks for item in check.targets})
    if normalized:
        selected = [check for check in checks if normalized in check.targets]
        if not selected:
            print(
                f"error: unknown validation target {target!r}; choose from: "
                + ", ".join(known_targets),
                file=sys.stderr,
            )
            return 2
    else:
        selected = checks
    context = CheckContext(repository_root())
    diagnostics = sorted(diagnostic for check in selected for diagnostic in check.run(context))
    for diagnostic in diagnostics:
        print(diagnostic.render())
    if diagnostics:
        print(f"validation failed: {len(diagnostics)} issue(s)", file=sys.stderr)
        return 1
    print(f"validation passed: {len(selected)} check(s)")
    return 0


def test(target: str) -> int:
    root = repository_root()
    normalized = _normalize_target(target).replace("-", "_")
    test_root = root / "tools" / "repo_maintenance" / "tests"
    if normalized:
        candidates = sorted(test_root.glob(f"test_*{normalized}*.py"))
        if not candidates:
            available = sorted(
                path.stem.removeprefix("test_").replace("_", "-")
                for path in test_root.glob("test_*.py")
            )
            print(
                f"error: unknown test target {target!r}; choose from: " + ", ".join(available),
                file=sys.stderr,
            )
            return 2
        paths = [str(path.relative_to(root)) for path in candidates]
    else:
        paths = [str(test_root.relative_to(root))]
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-c",
            "tools/maintenance/pyproject.toml",
            "-p",
            "no:cacheprovider",
            *paths,
        ],
        cwd=root,
        check=False,
    )
    return completed.returncode


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="python -m tools.repo_maintenance")
    subcommands = result.add_subparsers(dest="command", required=True)
    validate_parser = subcommands.add_parser("validate", help="run offline repository validators")
    validate_parser.add_argument("target", nargs="?", default="")
    test_parser = subcommands.add_parser("test", help="run deterministic maintenance tests")
    test_parser.add_argument("target", nargs="?", default="")
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.command == "validate":
        return validate(arguments.target)
    if arguments.command == "test":
        return test(arguments.target)
    raise AssertionError(f"unhandled command: {arguments.command}")
