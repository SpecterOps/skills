from __future__ import annotations

import os
import stat
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path

Replace = Callable[[str | Path, str | Path], None]


class InstallRollbackError(RuntimeError):
    """An output installation failed and at least one rollback also failed."""


def _ready_file(destination: Path, contents: bytes, mode: int, prefix: str) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=destination.parent, prefix=f".{destination.name}.{prefix}.", delete=False
    ) as handle:
        ready = Path(handle.name)
        handle.write(contents)
    ready.chmod(mode)
    return ready


def install_text_outputs(
    root: Path,
    outputs: Mapping[Path, str],
    *,
    replace: Replace = os.replace,
) -> None:
    """Atomically install a declared text-output set, rolling back partial installs."""
    originals: dict[Path, tuple[bytes | None, int]] = {}
    for relative in outputs:
        destination = root / relative
        if destination.is_file():
            originals[relative] = (
                destination.read_bytes(),
                stat.S_IMODE(destination.stat().st_mode),
            )
        else:
            originals[relative] = (None, 0o644)

    installed: list[Path] = []
    ready_paths: list[Path] = []
    try:
        for relative, contents in outputs.items():
            destination = root / relative
            ready = _ready_file(
                destination, contents.encode("utf-8"), originals[relative][1], "install"
            )
            ready_paths.append(ready)
            replace(ready, destination)
            ready_paths.remove(ready)
            installed.append(relative)
    except OSError as primary:
        rollback_errors: list[str] = []
        for relative in reversed(installed):
            destination = root / relative
            contents, mode = originals[relative]
            try:
                if contents is None:
                    destination.unlink(missing_ok=True)
                else:
                    restore = _ready_file(destination, contents, mode, "restore")
                    ready_paths.append(restore)
                    replace(restore, destination)
                    ready_paths.remove(restore)
            except OSError as rollback:
                rollback_errors.append(f"{relative.as_posix()}: {rollback}")
        if rollback_errors:
            raise InstallRollbackError(
                f"installation failed: {primary}; rollback failed: {'; '.join(rollback_errors)}"
            ) from primary
        raise
    finally:
        for ready in ready_paths:
            ready.unlink(missing_ok=True)
