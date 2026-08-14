from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

from tools.repo_maintenance import portability
from tools.repo_maintenance.checks import check_portability, check_provenance
from tools.repo_maintenance.models import CheckContext


@pytest.mark.parametrize(
    "value",
    [
        "/home/alice/project/output.json",
        "'/Users/alice/project/output.json'",
        "C:\\Users\\alice\\project\\output.json",
        r"C:\\Users\\alice\\project\\output.json",
    ],
)
def test_developer_home_patterns_cover_platform_and_quoting(value: str) -> None:
    assert any(pattern.search(value) for pattern in check_portability.HOME_PATTERNS)


@pytest.mark.parametrize(
    "value",
    [
        "/home/<user>/project",
        "/Users/${USER}/project",
        r"C:\Users\%USERNAME%\project",
        r"C:\Users\<target-user>\project",
    ],
)
def test_home_patterns_allow_placeholders_and_target_examples(value: str) -> None:
    assert not any(pattern.search(value) for pattern in check_portability.HOME_PATTERNS)


def test_authored_classification_excludes_references_and_assets() -> None:
    assert check_portability.is_authored(Path("plugins/demo/skills/example/scripts/run.sh"))
    assert not check_portability.is_authored(
        Path("plugins/demo/skills/example/references/synthetic.py")
    )
    assert not check_portability.is_authored(Path("plugins/demo/assets/vendor.js"))


def test_fixed_temporary_output_pattern_requires_unique_api() -> None:
    assert check_portability.FIXED_TEMP.search('log="/tmp/output.log"')
    assert not check_portability.FIXED_TEMP.search(
        'log="$(mktemp "${TMPDIR:-/tmp}/output.XXXXXX.log")"'
    )


def test_real_com_defaults_are_portable_and_koppeling_is_pinned(repo_root: Path) -> None:
    scripts = repo_root / "plugins/tradecraft-windows/skills/com-proxy-triage/scripts"
    watcher = (scripts / "Watch-InProcServer32Misses.ps1").read_text(encoding="utf-8")
    helper = (scripts / "ComHijackHost.Common.ps1").read_text(encoding="utf-8")
    assert "C:\\Users\\zach" not in watcher
    assert "[System.IO.Path]::GetTempPath()" in watcher
    assert "[Guid]::NewGuid()" in watcher
    assert "c2eafe11e6c31e1f64438a88d283ce3b0e4536a8" in helper
    assert "checkout --detach $expectedCommit" in helper
    assert "Assert-ComHijackKoppelingCommit" in helper


def test_powershell_paths_cross_process_boundary_through_environment(
    tmp_path: Path, monkeypatch
) -> None:
    script = tmp_path / "plugins/example/scripts/Path With Spaces.ps1"
    script.parent.mkdir(parents=True)
    script.write_text("Write-Output 'ok'\n", encoding="utf-8")
    calls = []

    def run(command, **options):
        calls.append((command, options))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(portability.shutil, "which", lambda name: "pwsh")
    monkeypatch.setattr(portability, "_psscriptanalyzer_version", lambda root: "1.25.0")
    monkeypatch.setattr(portability.subprocess, "run", run)

    assert portability.powershell(tmp_path) == 0
    path_calls = [
        options for _, options in calls if portability.POWERSHELL_PATH_ENV in options.get("env", {})
    ]
    assert len(path_calls) == 2
    for options in path_calls:
        assert options["env"][portability.POWERSHELL_PATH_ENV] == str(script.resolve())
    assert all(str(script) not in command for command, _ in calls)
    assert all("$args[0]" not in " ".join(command) for command, _ in calls)
    analysis = next(command for command, _ in calls if "Invoke-ScriptAnalyzer" in " ".join(command))
    assert "Import-Module PSScriptAnalyzer" in " ".join(analysis)
    assert "-RequiredVersion" in " ".join(analysis)


def test_powershell_rejects_an_unavailable_pinned_analyzer_version(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(portability.shutil, "which", lambda name: "pwsh")
    monkeypatch.setattr(portability, "_psscriptanalyzer_version", lambda root: "1.25.0")

    def run(command, **options):
        script = " ".join(command)
        returncode = 4 if "Get-Module -ListAvailable PSScriptAnalyzer" in script else 0
        return subprocess.CompletedProcess(command, returncode, "", "")

    monkeypatch.setattr(portability.subprocess, "run", run)

    assert portability.powershell(tmp_path) == 1
    assert "PSScriptAnalyzer 1.25.0 is required but not installed" in capsys.readouterr().out


def _provenance_root(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path
    schemas = root / "tools/maintenance/schemas"
    schemas.mkdir(parents=True)
    source = Path(__file__).parents[2] / "maintenance/schemas/provenance.schema.json"
    shutil.copyfile(source, schemas / "provenance.schema.json")
    artifact = root / "plugins/example/tool.exe"
    artifact.parent.mkdir(parents=True)
    artifact.write_bytes(b"MZ synthetic")
    relative = artifact.relative_to(root).as_posix()
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    (root / "tools/maintenance/provenance.toml").write_text(
        "\n".join(
            (
                "[[artifacts]]",
                f'path = "{relative}"',
                'source = "https://example.test/tool/1.0.0"',
                'immutable_ref = "1.0.0"',
                'build = "Synthetic fixture build."',
                'license_evidence = "https://example.test/tool/1.0.0/license"',
                f'sha256 = "{digest}"',
                'verification = "Synthetic fixture evidence."',
                "",
            )
        ),
        encoding="utf-8",
    )
    return root, relative


def test_provenance_accepts_complete_matching_inventory(tmp_path: Path, monkeypatch) -> None:
    root, relative = _provenance_root(tmp_path)
    monkeypatch.setattr(check_provenance, "_tracked_artifacts", lambda root: {relative})
    assert check_provenance.run(CheckContext(root)) == []


def test_provenance_reports_missing_stale_and_wrong_digest(tmp_path: Path, monkeypatch) -> None:
    root, relative = _provenance_root(tmp_path)
    config = root / "tools/maintenance/provenance.toml"
    config.write_text(
        config.read_text().replace('sha256 = "', 'sha256 = "' + "0" * 64 + "#"), encoding="utf-8"
    )
    monkeypatch.setattr(
        check_provenance,
        "_tracked_artifacts",
        lambda root: {"plugins/example/missing.dll"},
    )
    reasons = [item.reason for item in check_provenance.run(CheckContext(root))]
    assert any("lacks provenance" in reason for reason in reasons)
    assert any("stale" in reason for reason in reasons)
    assert any("SHA-256 mismatch" in reason for reason in reasons)


def test_provenance_reports_tracked_artifact_missing_from_worktree(
    tmp_path: Path, monkeypatch
) -> None:
    root, relative = _provenance_root(tmp_path)
    (root / relative).unlink()
    monkeypatch.setattr(check_provenance, "_tracked_artifacts", lambda root: {relative})

    reasons = [item.reason for item in check_provenance.run(CheckContext(root))]

    assert reasons == ["tracked artifact is missing or not a file in the worktree"]
