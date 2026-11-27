"""Import the reference ZIP produced by Cobalt Strike's resource exporter."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from contextlib import ExitStack
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from tools.repo_maintenance.transaction import install_text_outputs

SOURCE_REPOSITORY = "https://github.com/Cobalt-Strike/beacon-interpreter"
SKILL = Path("plugins/c2-cobaltstrike/skills/cobalt-strike-beacon-interpreter")
HEADERS = Path("references/interpreter-includes")
PROVENANCE = Path("references/provenance.json")
RESOURCES = {
    "LICENSE": Path("LICENSE"),
    "skills.md": Path("references/compatibility.md"),
    "interpreter_demo.c": Path("assets/interpreter_demo.c"),
}


def read_export(path: Path) -> dict[Path, str]:
    outputs = {}
    files = {}
    with ZipFile(path) as archive:
        revision = archive.comment.decode("ascii")
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("The ZIP comment must identify the exported Git commit")
        names = [entry.filename for entry in archive.infolist() if not entry.is_dir()]
        if len(names) != len({name.casefold() for name in names}):
            raise ValueError("The ZIP contains duplicate or case-colliding paths")
        missing = RESOURCES.keys() - set(names)
        if missing:
            raise ValueError(f"Missing upstream files: {', '.join(sorted(missing))}")
        for source in sorted(names):
            destination = RESOURCES.get(source)
            if destination is None:
                header = PurePosixPath(source)
                if not re.fullmatch(r"interpreter-includes/[A-Za-z0-9_.-]+\.h", source):
                    raise ValueError(f"Unexpected upstream file: {source}")
                destination = HEADERS / header.name
            content = archive.read(source).replace(b"\r\n", b"\n")
            outputs[destination] = content.decode("utf-8")
            files[destination.as_posix()] = {
                "source": source,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
    if not any(destination.parent == HEADERS for destination in outputs):
        raise ValueError("The ZIP does not contain any Interpreter headers")
    provenance = {
        "source_repository": SOURCE_REPOSITORY,
        "source_revision": revision,
        "hash_format": "sha256 with CRLF normalized to LF",
        "files": {name: files[name] for name in sorted(files, key=str.casefold)},
    }
    outputs[PROVENANCE] = json.dumps(provenance, indent=2) + "\n"
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="ZIP from the upstream resource exporter")
    parser.add_argument("--check", action="store_true", help="Verify without writing files")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[2] / SKILL
    try:
        outputs = read_export(args.archive)
        stale = {path.relative_to(skill) for path in (skill / HEADERS).glob("*.h")} - outputs.keys()
        if args.check:
            differences = stale | {
                path
                for path, text in outputs.items()
                if not (skill / path).is_file()
                or (skill / path).read_text(encoding="utf-8") != text
            }
            if differences:
                names = ", ".join(sorted(path.as_posix() for path in differences))
                raise ValueError(f"Imported resources differ from the ZIP: {names}")
        else:
            with ExitStack() as rollback:
                for path in sorted(stale):
                    destination = skill / path
                    contents = destination.read_bytes()
                    destination.unlink()
                    rollback.callback(destination.write_bytes, contents)
                install_text_outputs(skill, outputs)
                rollback.pop_all()
    except (BadZipFile, OSError, ValueError) as error:
        parser.exit(1, f"Could not refresh the Interpreter resources: {error}\n")


if __name__ == "__main__":
    main()
