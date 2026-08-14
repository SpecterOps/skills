from __future__ import annotations

import subprocess
from pathlib import Path


class RepositoryDiscoveryError(RuntimeError):
    """Repository inputs could not be enumerated."""


def repository_files(root: Path) -> list[Path]:
    """Return tracked and nonignored untracked files, including hidden paths."""
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RepositoryDiscoveryError(f"git ls-files failed: {detail}")
    paths = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(raw_path.decode("utf-8"))
        path = root / relative
        if path.is_file():
            paths.append(path)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()
