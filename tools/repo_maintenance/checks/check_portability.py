from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from tools.repo_maintenance.files import relative_path, repository_files
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic

TEXT_SUFFIXES = {".cjs", ".js", ".json", ".ps1", ".py", ".sh", ".toml", ".yaml", ".yml"}
HOME_PATTERNS = (
    re.compile(r"/(?:Users|home)/(?![<$'{])[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\+Users\\+(?![<%$'{])[A-Za-z0-9._-]+\\+", re.IGNORECASE),
)
FIXED_TEMP = re.compile(r"(?:>|=)\s*['\"]?(?:/tmp/|[A-Za-z]:\\+Temp\\+)[^\s'\"]+", re.IGNORECASE)


def is_authored(relative: Path) -> bool:
    if not relative.parts or relative.parts[0] != "plugins":
        return False
    if "references" in relative.parts or "assets" in relative.parts:
        return False
    if relative.suffix.lower() not in TEXT_SUFFIXES:
        return False
    return (
        "scripts" in relative.parts
        or "OpenTelemetry" in relative.parts
        or relative.name
        in {
            "plugin.json",
            "ownership.json",
        }
    )


def _git_modes(root: Path) -> dict[str, str]:
    completed = subprocess.run(
        ["git", "ls-files", "-s", "-z", "--", "plugins"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        return {}
    result = {}
    for record in completed.stdout.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        result[raw_path.decode("utf-8")] = metadata.split()[0].decode("ascii")
    changed = subprocess.run(
        ["git", "diff", "--raw", "-z", "--", "plugins"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if changed.returncode == 0:
        records = changed.stdout.split(b"\0")
        for index in range(0, len(records) - 1, 2):
            metadata = records[index]
            raw_path = records[index + 1]
            if not metadata or not raw_path:
                continue
            fields = metadata.removeprefix(b":").split()
            result[raw_path.decode("utf-8")] = fields[1].decode("ascii")
    return result


def _syntax(root: Path, path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".sh":
        command = ["bash", "-n", str(path)]
    elif suffix in {".js", ".cjs"}:
        node = shutil.which("node")
        if node is None:
            return None
        command = [node, "--check", str(path)]
    else:
        return None
    completed = subprocess.run(command, cwd=root, check=False, capture_output=True, text=True)
    if completed.returncode:
        return (completed.stderr or completed.stdout).strip()
    return None


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    files = repository_files(context.root)
    folded: dict[str, str] = {}
    for path in files:
        relative = Path(relative_path(context.root, path))
        key = relative.as_posix().casefold()
        previous = folded.get(key)
        if previous is not None and previous != relative.as_posix():
            diagnostics.append(
                Diagnostic(
                    "portability.casefold",
                    relative.as_posix(),
                    f"case-fold path collision with {previous}",
                )
            )
        folded[key] = relative.as_posix()

    modes = _git_modes(context.root)
    for path in files:
        relative = Path(relative_path(context.root, path))
        if not is_authored(relative):
            continue
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except UnicodeError as exc:
            diagnostics.append(Diagnostic("portability.encoding", relative.as_posix(), str(exc)))
            continue
        if b"\r\n" in raw:
            diagnostics.append(
                Diagnostic(
                    "portability.line-endings", relative.as_posix(), "authored file uses CRLF"
                )
            )
        for pattern in HOME_PATTERNS:
            match = pattern.search(text)
            if match:
                diagnostics.append(
                    Diagnostic(
                        "portability.home-path",
                        relative.as_posix(),
                        f"developer-specific home path {match.group(0)!r}",
                    )
                )
        match = FIXED_TEMP.search(text)
        if match:
            diagnostics.append(
                Diagnostic(
                    "portability.temp-path",
                    relative.as_posix(),
                    f"fixed temporary output {match.group(0)!r}; use a unique platform API",
                )
            )
        if text.startswith("#!") and modes.get(relative.as_posix()) != "100755":
            diagnostics.append(
                Diagnostic(
                    "portability.executable-mode",
                    relative.as_posix(),
                    "authored shebang script is not executable in the Git index",
                )
            )
        failure = _syntax(context.root, path)
        if failure:
            diagnostics.append(Diagnostic("portability.syntax", relative.as_posix(), failure))
    return diagnostics


CHECK = CheckSpec("portability.core", frozenset({"portability"}), run)
