from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

from tools.repo_maintenance.checks import check_portability, check_provenance
from tools.repo_maintenance.policy import toolchain

POWERSHELL_PATH_ENV = "REPO_MAINTENANCE_POWERSHELL_PATH"
PSSCRIPTANALYZER_VERSION_ENV = "REPO_MAINTENANCE_PSSCRIPTANALYZER_VERSION"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _render(diagnostics) -> int:
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


def _powershell_environment(
    *, path: Path | None = None, analyzer_version: str | None = None
) -> dict[str, str]:
    environment = os.environ.copy()
    if path is not None:
        environment[POWERSHELL_PATH_ENV] = str(path.resolve())
    if analyzer_version is not None:
        environment[PSSCRIPTANALYZER_VERSION_ENV] = analyzer_version
    return environment


def _psscriptanalyzer_version(root: Path) -> str:
    tools = toolchain(root).get("tools")
    version = tools.get("psscriptanalyzer") if isinstance(tools, dict) else None
    if not isinstance(version, str) or not version:
        raise ValueError("toolchain PSScriptAnalyzer version must be a non-empty string")
    return version


def powershell(root: Path) -> int:
    executable = shutil.which("pwsh")
    if executable is None:
        print("optional  powershell syntax: SKIP (pwsh not installed)")
        print("optional  PSScriptAnalyzer: SKIP (PowerShell unavailable)")
        return 0
    try:
        analyzer_version = _psscriptanalyzer_version(root)
    except (OSError, ValueError) as exc:
        print(f"error: failed to load PSScriptAnalyzer version: {exc}")
        return 1
    parser_script = (
        "$tokens=$null; $errors=$null; "
        "[System.Management.Automation.Language.Parser]::ParseFile("
        f"$env:{POWERSHELL_PATH_ENV},[ref]$tokens,[ref]$errors) > $null; "
        "if ($errors.Count) { $errors | ForEach-Object { $_.ToString() }; exit 1 }"
    )
    failed = False
    paths = sorted(root.glob("plugins/**/*.ps1"))
    for path in paths:
        completed = subprocess.run(
            [executable, "-NoLogo", "-NoProfile", "-Command", parser_script],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            env=_powershell_environment(path=path),
        )
        if completed.returncode:
            failed = True
            detail = (completed.stderr or completed.stdout).strip()
            print(f"powershell.syntax: {path.relative_to(root).as_posix()}: {detail}")
    analyzer = subprocess.run(
        [
            executable,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            "$available = @(Get-Module -ListAvailable PSScriptAnalyzer); "
            "if (-not $available) { exit 3 }; "
            "if ($available | Where-Object { "
            f"$_.Version.ToString() -eq $env:{PSSCRIPTANALYZER_VERSION_ENV} "
            "}) "
            "{ exit 0 } else { exit 4 }",
        ],
        cwd=root,
        check=False,
        env=_powershell_environment(analyzer_version=analyzer_version),
    )
    if analyzer.returncode == 3:
        print("optional  PSScriptAnalyzer: SKIP (module not installed)")
    elif analyzer.returncode:
        if analyzer.returncode == 4:
            print(
                f"error: PSScriptAnalyzer {analyzer_version} is required but not installed",
                flush=True,
            )
        else:
            print("error: failed to detect PSScriptAnalyzer", flush=True)
        failed = True
    else:
        for path in paths:
            completed = subprocess.run(
                [
                    executable,
                    "-NoLogo",
                    "-NoProfile",
                    "-Command",
                    "$module = Import-Module PSScriptAnalyzer "
                    f"-RequiredVersion $env:{PSSCRIPTANALYZER_VERSION_ENV} "
                    "-Force -PassThru -ErrorAction Stop; "
                    f"if ($module.Version.ToString() -ne $env:{PSSCRIPTANALYZER_VERSION_ENV}) "
                    "{ throw 'Unexpected PSScriptAnalyzer version loaded' }; "
                    f"Invoke-ScriptAnalyzer -Path $env:{POWERSHELL_PATH_ENV} -Severity Error | "
                    "Format-Table -AutoSize | Out-String -Width 240",
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                env=_powershell_environment(path=path, analyzer_version=analyzer_version),
            )
            output = completed.stdout.strip()
            if completed.returncode or output:
                failed = True
                print(
                    f"powershell.analysis: {path.relative_to(root).as_posix()}: "
                    f"{output or completed.stderr.strip()}"
                )
    if not failed:
        print(f"PowerShell syntax passed: {len(paths)} file(s)")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run repository portability checks")
    parser.add_argument("command", choices=("check", "provenance", "powershell"))
    arguments = parser.parse_args(argv)
    root = repository_root()
    if arguments.command == "check":
        if shutil.which("node") is None:
            print("optional  node syntax: SKIP (node not installed)")
        return _render(check_portability.run(check_portability.CheckContext(root)))
    if arguments.command == "provenance":
        return _render(check_provenance.run(check_provenance.CheckContext(root)))
    return powershell(root)


if __name__ == "__main__":
    raise SystemExit(main())
