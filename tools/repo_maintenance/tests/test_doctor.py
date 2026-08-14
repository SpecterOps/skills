from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _tool(directory: Path, name: str, output: str) -> None:
    path = directory / name
    path.write_text(f"#!/bin/sh\nprintf '%s\\n' '{output}'\n", encoding="utf-8")
    path.chmod(0o755)


def _doctor(repo_root: Path, tmp_path: Path, include_uv: bool) -> subprocess.CompletedProcess[str]:
    just = shutil.which("just")
    bash = shutil.which("bash")
    assert just is not None
    assert bash is not None
    python = shutil.which("python3.13")
    assert python is not None
    (tmp_path / "bash").symlink_to(bash)
    (tmp_path / "python3.13").symlink_to(python)
    _tool(tmp_path, "just", "just 1.58.0")
    if include_uv:
        _tool(tmp_path, "uv", "uv 0.12.4")
    environment = os.environ.copy()
    environment["PATH"] = str(tmp_path)
    environment["MAINTENANCE_PYTHON"] = "python3.13"
    environment["UV_BOOTSTRAP_ENV"] = str(tmp_path / "isolated-bootstrap")
    return subprocess.run(
        [just, "doctor"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


def test_doctor_fails_when_required_tool_is_missing(repo_root: Path, tmp_path: Path) -> None:
    completed = _doctor(repo_root, tmp_path, include_uv=False)
    assert completed.returncode == 1
    assert "required  uv: MISSING" in completed.stdout


def test_doctor_allows_missing_optional_tools(repo_root: Path, tmp_path: Path) -> None:
    completed = _doctor(repo_root, tmp_path, include_uv=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "optional  shellcheck: SKIP" in completed.stdout
    assert "optional  powershell: SKIP" in completed.stdout
