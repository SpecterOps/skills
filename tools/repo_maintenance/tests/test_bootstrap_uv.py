from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance import bootstrap_uv


def test_installed_version_accepts_platform_suffix(tmp_path: Path) -> None:
    executable = tmp_path / "uv"
    executable.write_text(
        "#!/bin/sh\nprintf '%s\\n' 'uv 0.12.3 (synthetic-platform)'\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    assert bootstrap_uv.installed_version(executable) == "0.12.3"


def test_environment_override_stays_outside_project(
    repo_root: Path, tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("UV_BOOTSTRAP_ENV", str(tmp_path / "bootstrap"))
    version, environment = bootstrap_uv.configuration(repo_root)
    assert version == "0.12.3"
    assert environment == tmp_path / "bootstrap"
