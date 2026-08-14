from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance.checks import check_secrets
from tools.repo_maintenance.models import CheckContext


def test_secret_check_reports_location_without_echoing_value(tmp_path: Path, monkeypatch) -> None:
    document = tmp_path / "config.txt"
    value = "AK" + "IA" + "A" * 16
    document.write_text("safe\ncredential=" + value + "\n", encoding="utf-8")
    monkeypatch.setattr(check_secrets, "repository_files", lambda root: [document])
    diagnostics = check_secrets.run(CheckContext(tmp_path))
    assert len(diagnostics) == 1
    assert diagnostics[0].line == 2
    assert value not in diagnostics[0].render()


def test_secret_check_skips_binary_files(tmp_path: Path, monkeypatch) -> None:
    document = tmp_path / "asset.bin"
    document.write_bytes(b"\xff\xfe\x00")
    monkeypatch.setattr(check_secrets, "repository_files", lambda root: [document])
    assert check_secrets.run(CheckContext(tmp_path)) == []
