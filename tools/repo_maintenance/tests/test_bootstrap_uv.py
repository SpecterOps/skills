from __future__ import annotations

from pathlib import Path

import pytest

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


def test_find_uv_accepts_only_the_pinned_system_version(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    executable = tmp_path / "uv"
    executable.write_text("#!/bin/sh\nprintf '%s\\n' 'uv 99.0.0'\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("UV_BOOTSTRAP_ENV", str(tmp_path / "missing-bootstrap"))
    monkeypatch.setattr(bootstrap_uv.shutil, "which", lambda name: str(executable))

    with pytest.raises(RuntimeError, match=r"uv 0\.12\.3 is required.*reports 99\.0\.0"):
        bootstrap_uv.find_uv(repo_root)


def test_find_uv_accepts_the_pinned_system_version(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    executable = tmp_path / "uv"
    executable.write_text("#!/bin/sh\nprintf '%s\\n' 'uv 0.12.3'\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("UV_BOOTSTRAP_ENV", str(tmp_path / "missing-bootstrap"))
    monkeypatch.setattr(bootstrap_uv.shutil, "which", lambda name: str(executable))

    assert bootstrap_uv.find_uv(repo_root) == executable
