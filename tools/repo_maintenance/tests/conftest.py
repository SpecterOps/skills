from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()
