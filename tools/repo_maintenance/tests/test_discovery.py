from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from tools.repo_maintenance.discovery import DiscoveryError, discover_checks

MODULE_TEMPLATE = """\
from tools.repo_maintenance.models import CheckSpec

def run(context):
    return []

CHECK = CheckSpec({check_id!r}, frozenset({{{target!r}}}), run)
"""


def _package(tmp_path: Path, name: str, modules: dict[str, str]) -> str:
    package = tmp_path / name
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    for module_name, content in modules.items():
        (package / f"{module_name}.py").write_text(content, encoding="utf-8")
    return name


def test_new_check_module_is_discovered_without_registration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    package = _package(
        tmp_path,
        "synthetic_checks",
        {
            "check_zeta": MODULE_TEMPLATE.format(check_id="zeta", target="core"),
            "check_alpha": MODULE_TEMPLATE.format(check_id="alpha", target="core"),
            "helper": "raise RuntimeError('helpers must not be imported')\n",
        },
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    assert [check.check_id for check in discover_checks(package)] == ["alpha", "zeta"]


def test_duplicate_check_ids_fail_clearly(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    package = _package(
        tmp_path,
        "duplicate_checks",
        {
            "check_one": MODULE_TEMPLATE.format(check_id="same", target="core"),
            "check_two": MODULE_TEMPLATE.format(check_id="same", target="core"),
        },
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    with pytest.raises(DiscoveryError, match="duplicate check id 'same'"):
        discover_checks(package)
    for name in tuple(sys.modules):
        if name == package or name.startswith(f"{package}."):
            sys.modules.pop(name)


def test_import_failure_names_the_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    package = _package(
        tmp_path,
        "broken_checks",
        {"check_broken": "raise RuntimeError('synthetic failure')\n"},
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    with pytest.raises(DiscoveryError, match=r"broken_checks\.check_broken"):
        discover_checks(package)
