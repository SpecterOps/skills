from __future__ import annotations

import socket
import subprocess
import sys

import pytest

from tools.repo_maintenance.discovery import discover_checks
from tools.repo_maintenance.models import CheckContext


def test_offline_checks_do_not_open_network_connections(repo_root, monkeypatch) -> None:
    def blocked(*args, **kwargs):
        raise AssertionError("offline maintenance check attempted network access")

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    monkeypatch.setattr(socket.socket, "connect", blocked)
    diagnostics = [
        diagnostic
        for check in discover_checks()
        for diagnostic in check.run(CheckContext(repo_root))
    ]
    assert diagnostics == []


def test_validation_preserves_dirty_worktree(repo_root) -> None:
    before = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    completed = subprocess.run(
        [sys.executable, "-m", "tools.repo_maintenance", "validate"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    after = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert after == before


@pytest.mark.parametrize(
    "candidate",
    [
        ".venv/example",
        "tools/maintenance/.bootstrap-venv/example",
        "package/__pycache__/module.pyc",
        ".pytest_cache/state",
        ".ruff_cache/state",
        "reports/codex-example.md",
    ],
)
def test_generated_local_files_are_ignored(repo_root, candidate: str) -> None:
    completed = subprocess.run(
        ["git", "check-ignore", "--no-index", candidate],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, candidate
