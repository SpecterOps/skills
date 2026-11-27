from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

import pytest

from tools.repo_maintenance import import_beacon_interpreter_resources as importer


def make_export(path: Path, header: str = "interpreter-includes/beacon.h") -> Path:
    with ZipFile(path, "w") as archive:
        archive.comment = b"a" * 40
        archive.writestr("LICENSE", "license\n")
        archive.writestr("skills.md", "guide\n")
        archive.writestr("interpreter_demo.c", "demo\n")
        archive.writestr(header, "header\r\n")
    return path


def test_import_maps_upstream_resources_and_records_provenance(tmp_path: Path) -> None:
    outputs = importer.read_export(make_export(tmp_path / "resources.zip"))
    header = importer.HEADERS / "beacon.h"
    assert outputs[header] == "header\n"
    assert outputs[Path("references/compatibility.md")] == "guide\n"
    assert outputs[Path("assets/interpreter_demo.c")] == "demo\n"
    assert outputs[Path("LICENSE")] == "license\n"
    provenance = json.loads(outputs[importer.PROVENANCE])
    assert provenance["source_revision"] == "a" * 40
    assert provenance["files"][header.as_posix()] == {
        "source": "interpreter-includes/beacon.h",
        "sha256": hashlib.sha256(b"header\n").hexdigest(),
    }


def test_import_rejects_paths_outside_the_header_directory(tmp_path: Path) -> None:
    archive = make_export(tmp_path / "resources.zip", "interpreter-includes/../../invalid.h")
    with pytest.raises(ValueError, match="Unexpected upstream file"):
        importer.read_export(archive)
