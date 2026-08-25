#!/usr/bin/env python3
"""Create a go-review run directory and build its AST inventory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--scope-subpath", default=".")
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    script_root = Path(__file__).resolve().parent
    output_dir = args.output_dir.resolve()
    for name in ("findings", "findings-index.d", "coverage"):
        (output_dir / name).mkdir(parents=True, exist_ok=True)
    inventory_path = output_dir / "go-inventory.json"
    with tempfile.TemporaryDirectory(prefix="go-review-gocache-") as go_cache:
        environment = os.environ.copy()
        environment["GOCACHE"] = go_cache
        completed = subprocess.run(
            [
                "go",
                "run",
                str(script_root / "go_inventory.go"),
                "--repo-root",
                str(args.repo_root.resolve()),
                "--scope-subpath",
                args.scope_subpath,
                "--output",
                str(inventory_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
    if completed.returncode:
        sys.stderr.write(completed.stderr)
        return completed.returncode
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    summary = inventory.get("summary", {})
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "inventory_path": str(inventory_path),
                "go_file_count": summary.get("go_file_count", 0),
                "package_count": summary.get("package_count", 0),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
