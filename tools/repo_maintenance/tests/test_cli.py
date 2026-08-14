from __future__ import annotations

import subprocess

from tools.repo_maintenance import cli


def test_unknown_validation_target_fails(capsys) -> None:
    assert cli.validate("not-a-real-target") == 2
    assert "unknown validation target" in capsys.readouterr().err


def test_unknown_test_target_fails(capsys) -> None:
    assert cli.test("not-a-real-target") == 2
    assert "unknown test target" in capsys.readouterr().err


def test_bare_just_lists_available_commands(repo_root) -> None:
    completed = subprocess.run(
        ["just"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Available recipes:" in completed.stdout
    for recipe in ("bootstrap-uv", "doctor", "setup", "fmt-check", "validate", "test", "check"):
        assert recipe in completed.stdout
