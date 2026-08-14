from __future__ import annotations

import os
from pathlib import Path

import pytest

from tools.repo_maintenance.transaction import InstallRollbackError, install_text_outputs


def test_transaction_recreates_outputs_and_preserves_existing_modes(tmp_path: Path) -> None:
    existing = tmp_path / "existing.txt"
    existing.write_text("old", encoding="utf-8")
    existing.chmod(0o640)

    install_text_outputs(
        tmp_path,
        {Path("existing.txt"): "new", Path("nested/new.txt"): "created"},
    )

    assert existing.read_text() == "new"
    assert existing.stat().st_mode & 0o777 == 0o640
    assert (tmp_path / "nested/new.txt").read_text() == "created"
    assert (tmp_path / "nested/new.txt").stat().st_mode & 0o777 == 0o644


def test_transaction_rolls_back_partial_install(tmp_path: Path) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("first-old", encoding="utf-8")
    second.write_text("second-old", encoding="utf-8")
    calls = 0

    def fail_second(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic failure")
        os.replace(source, destination)

    with pytest.raises(OSError, match="synthetic failure"):
        install_text_outputs(
            tmp_path,
            {Path("first.txt"): "first-new", Path("second.txt"): "second-new"},
            replace=fail_second,
        )

    assert first.read_text() == "first-old"
    assert second.read_text() == "second-old"


def test_transaction_reports_rollback_failure(tmp_path: Path) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("first-old", encoding="utf-8")
    second.write_text("second-old", encoding="utf-8")
    calls = 0

    def fail_install_and_rollback(source, destination):
        nonlocal calls
        calls += 1
        if calls >= 2:
            raise OSError(f"failure {calls}")
        os.replace(source, destination)

    with pytest.raises(InstallRollbackError, match="rollback failed"):
        install_text_outputs(
            tmp_path,
            {Path("first.txt"): "first-new", Path("second.txt"): "second-new"},
            replace=fail_install_and_rollback,
        )
