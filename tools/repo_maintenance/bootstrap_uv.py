from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tomllib
import venv
from pathlib import Path


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def configuration(root: Path) -> tuple[str, Path]:
    project_root = root / "tools" / "maintenance"
    project = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    settings = project["tool"]["repo-maintenance"]
    version = settings["uv-version"]
    configured = os.environ.get("UV_BOOTSTRAP_ENV", settings["bootstrap-environment"])
    environment = Path(configured)
    if not environment.is_absolute():
        environment = project_root / environment
    return version, environment


def environment_uv(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "uv.exe"
    return environment / "bin" / "uv"


def environment_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def installed_version(executable: Path) -> str | None:
    if not executable.is_file():
        return None
    completed = subprocess.run(
        [str(executable), "--version"], check=False, capture_output=True, text=True
    )
    if completed.returncode:
        return None
    fields = completed.stdout.strip().split()
    return fields[1] if len(fields) >= 2 and fields[0] == "uv" else None


def ensure(root: Path) -> Path:
    version, environment = configuration(root)
    executable = environment_uv(environment)
    if installed_version(executable) == version:
        print(f"bootstrapped uv {version} is already available at {executable}")
        return executable
    venv.EnvBuilder(with_pip=True, clear=False).create(environment)
    subprocess.run(
        [
            str(environment_python(environment)),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--only-binary=:all:",
            f"uv=={version}",
        ],
        cwd=root,
        check=True,
    )
    if installed_version(executable) != version:
        raise RuntimeError(f"uv {version} was installed but could not be verified at {executable}")
    print(f"bootstrapped uv {version} at {executable}")
    return executable


def find_uv(root: Path) -> Path:
    version, environment = configuration(root)
    executable = environment_uv(environment)
    if installed_version(executable) == version:
        return executable
    system_uv = shutil.which("uv")
    if system_uv:
        system_executable = Path(system_uv)
        system_version = installed_version(system_executable)
        if system_version == version:
            return system_executable
        found = system_version or "unknown"
        raise RuntimeError(
            f"uv {version} is required, but {system_executable} reports {found}; "
            "run 'just bootstrap-uv'"
        )
    raise RuntimeError("uv is unavailable; run 'just bootstrap-uv' or install uv")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage the pinned, Git-ignored uv bootstrap")
    parser.add_argument("command", choices=("ensure", "path"))
    arguments = parser.parse_args(argv)
    try:
        executable = (
            ensure(repository_root())
            if arguments.command == "ensure"
            else find_uv(repository_root())
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if arguments.command == "path":
        print(executable)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
