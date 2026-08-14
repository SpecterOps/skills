from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from tools.repo_maintenance.checks import check_portability, check_provenance


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _render(diagnostics) -> int:
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


def powershell(root: Path) -> int:
    executable = shutil.which("pwsh")
    if executable is None:
        print("optional  powershell syntax: SKIP (pwsh not installed)")
        print("optional  PSScriptAnalyzer: SKIP (PowerShell unavailable)")
        return 0
    parser_script = (
        "$tokens=$null; $errors=$null; "
        "[System.Management.Automation.Language.Parser]::ParseFile("
        "$args[0],[ref]$tokens,[ref]$errors) > $null; "
        "if ($errors.Count) { $errors | ForEach-Object { $_.ToString() }; exit 1 }"
    )
    failed = False
    paths = sorted(root.glob("plugins/**/*.ps1"))
    for path in paths:
        completed = subprocess.run(
            [executable, "-NoLogo", "-NoProfile", "-Command", parser_script, str(path)],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
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
            "if (Get-Module -ListAvailable PSScriptAnalyzer) { exit 0 } else { exit 3 }",
        ],
        check=False,
    )
    if analyzer.returncode == 3:
        print("optional  PSScriptAnalyzer: SKIP (module not installed)")
    elif analyzer.returncode:
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
                    "Invoke-ScriptAnalyzer -Path $args[0] -Severity Error | "
                    "Format-Table -AutoSize | Out-String -Width 240",
                    str(path),
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
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
