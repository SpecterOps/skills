from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.repo_maintenance.generators import catalog


def _fixture(
    tmp_path: Path,
    *,
    status: str = "active",
    surfaces: tuple[str, ...] = ("codex", "claude"),
    capability: bool = True,
    claude_manifest: bool = True,
    duplicate: bool = False,
) -> Path:
    root = tmp_path
    schemas = root / "tools/maintenance/schemas"
    schemas.mkdir(parents=True)
    source_schemas = Path(__file__).parents[2] / "maintenance/schemas"
    for name in ("catalog", "ownership", "codex-plugin", "claude-plugin"):
        shutil.copyfile(source_schemas / f"{name}.schema.json", schemas / f"{name}.schema.json")
    quoted_surfaces = ", ".join(json.dumps(item) for item in surfaces)
    declaration = f'[[plugins]]\nname = "example"\nsurfaces = [{quoted_surfaces}]\n'
    (root / "tools/maintenance/catalog.toml").write_text(
        "version = 1\n\n" + declaration + ("\n" + declaration if duplicate else ""),
        encoding="utf-8",
    )
    plugin = root / "plugins/example"
    (plugin / ".codex-plugin").mkdir(parents=True)
    codex = {
        "name": "example",
        "version": "1.2.3",
        "description": "Synthetic plugin.",
        "author": {},
        "license": "UNLICENSED",
        "keywords": [],
        "skills": "./skills/",
        "interface": {
            "displayName": "Example",
            "shortDescription": "Synthetic plugin.",
            "longDescription": "Synthetic plugin for catalog tests.",
            "developerName": "Test",
            "category": "Testing",
            "capabilities": [],
            "defaultPrompt": [],
            "brandColor": "#000000",
            "composerIcon": "./icon.svg",
            "logo": "./icon.svg",
        },
    }
    (plugin / ".codex-plugin/plugin.json").write_text(json.dumps(codex), encoding="utf-8")
    if claude_manifest:
        (plugin / ".claude-plugin").mkdir()
        claude = {key: codex[key] for key in ("name", "version", "description")}
        claude["author"] = {}
        (plugin / ".claude-plugin/plugin.json").write_text(json.dumps(claude), encoding="utf-8")
    skills = ["working"] if capability else []
    if capability:
        skill = plugin / "skills/working"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: working\ndescription: Works.\n---\n", encoding="utf-8"
        )
    ownership = {
        "plugin": "example",
        "purpose": "Synthetic plugin.",
        "status": status,
        "agents": [],
        "skills": skills,
    }
    (plugin / "ownership.json").write_text(json.dumps(ownership), encoding="utf-8")
    (root / "agents").mkdir()
    (root / ".agents/plugins").mkdir(parents=True)
    (root / ".claude-plugin").mkdir()
    (root / ".agents/plugins/marketplace.json").write_text("{}\n", encoding="utf-8")
    (root / ".claude-plugin/marketplace.json").write_text("{}\n", encoding="utf-8")
    (root / "README.md").write_text(
        f"before\n{catalog.BEGIN}\nstale\n{catalog.END}\nafter\n", encoding="utf-8"
    )
    return root


def _reasons(root: Path) -> list[str]:
    return [diagnostic.reason for diagnostic in catalog.inspect(root)[1]]


def test_active_plugin_must_have_a_capability(tmp_path: Path) -> None:
    root = _fixture(tmp_path, capability=False)
    assert "active plugin has no packaged capability" in _reasons(root)


def test_incubating_plugin_cannot_be_published_to_claude(tmp_path: Path) -> None:
    root = _fixture(tmp_path, status="incubating", capability=False)
    assert any("cannot be published to Claude" in reason for reason in _reasons(root))


def test_incubating_plugin_can_prepare_an_unpublished_claude_manifest(tmp_path: Path) -> None:
    root = _fixture(
        tmp_path,
        status="incubating",
        surfaces=("codex",),
        capability=False,
        claude_manifest=True,
    )

    assert _reasons(root) == []


def test_declared_surface_requires_its_manifest(tmp_path: Path) -> None:
    root = _fixture(tmp_path, claude_manifest=False)
    assert "required claude manifest is missing" in _reasons(root)


def test_release_version_must_match_the_canonical_manifest(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    path = root / "plugins/example/ownership.json"
    ownership = json.loads(path.read_text(encoding="utf-8"))
    ownership["release"] = {"version": "9.9.9", "channel": "stable"}
    path.write_text(json.dumps(ownership), encoding="utf-8")

    assert "release version must match the canonical Codex manifest" in _reasons(root)


def test_duplicate_catalog_order_is_rejected(tmp_path: Path) -> None:
    root = _fixture(tmp_path, duplicate=True)
    assert "duplicate plugin order entry 'example'" in _reasons(root)


def test_stale_generated_outputs_are_reported(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    diagnostics = catalog.check(root)
    assert {item.path for item in diagnostics} == {
        ".agents/plugins/marketplace.json",
        ".claude-plugin/marketplace.json",
        "README.md",
    }


def test_generation_is_idempotent_and_preserves_readme_prose(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    catalog.generate(root)
    first = {relative: (root / relative).read_bytes() for relative in catalog.OUTPUTS}
    catalog.generate(root)
    second = {relative: (root / relative).read_bytes() for relative in catalog.OUTPUTS}

    assert first == second
    readme = second[Path("README.md")].decode()
    assert readme.startswith("before\n")
    assert readme.endswith("\nafter\n")


def test_generation_recreates_a_missing_output(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    missing = root / ".agents/plugins/marketplace.json"
    missing.unlink()

    catalog.generate(root)

    assert missing.is_file()
    assert catalog.check(root) == []


def test_generation_preserves_output_modes(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    expected_modes = {}
    for index, relative in enumerate(catalog.OUTPUTS):
        mode = 0o640 + index
        path = root / relative
        path.chmod(mode)
        expected_modes[relative] = mode

    catalog.generate(root)

    assert {
        relative: (root / relative).stat().st_mode & 0o777 for relative in catalog.OUTPUTS
    } == expected_modes


def test_failed_install_restores_every_catalog_output(tmp_path: Path, monkeypatch) -> None:
    root = _fixture(tmp_path)
    before = {relative: (root / relative).read_bytes() for relative in catalog.OUTPUTS}
    real_replace = catalog.os.replace
    calls = 0

    def fail_second(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic install failure")
        return real_replace(source, destination)

    monkeypatch.setattr(catalog.os, "replace", fail_second)
    try:
        catalog.generate(root)
    except OSError as exc:
        assert "synthetic install failure" in str(exc)
    else:
        raise AssertionError("catalog generation unexpectedly succeeded")

    after = {relative: (root / relative).read_bytes() for relative in catalog.OUTPUTS}
    assert after == before
    assert not list(root.rglob(".*.restore.*"))
    assert not list(root.rglob(".*.json.*"))
