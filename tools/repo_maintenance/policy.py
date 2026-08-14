from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

RECIPE = re.compile(r"^([a-zA-Z][a-zA-Z0-9_-]*)(?:\s+[^:]*)?:")


def load_toml_mapping(path: Path) -> dict[str, Any]:
    value = tomllib.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a TOML mapping")
    return value


def toolchain(root: Path) -> dict[str, Any]:
    return load_toml_mapping(root / "tools/maintenance/toolchain.toml")


def public_recipes(root: Path) -> set[str]:
    paths = [root / "justfile", *sorted((root / "tools/maintenance/just").glob("*.just"))]
    result: set[str] = set()
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if ":=" in line:
                continue
            match = RECIPE.match(line)
            if match and not match.group(1).startswith("_"):
                result.add(match.group(1))
    return result
