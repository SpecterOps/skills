from __future__ import annotations

from pathlib import Path

from tools.repo_maintenance.generators import inventory


def test_real_inventory_is_current(repo_root: Path) -> None:
    assert inventory.check(repo_root) == []


def test_inventory_contains_every_discovered_skill_and_agent(repo_root: Path) -> None:
    text, diagnostics = inventory.expected(repo_root)
    assert diagnostics == []
    assert text is not None
    for path in repo_root.glob("plugins/*/skills/*/SKILL.md"):
        assert f"`{path.parent.name}`" in text
    for path in (repo_root / "agents").glob("*.toml"):
        assert f"`{path.stem}`" in text


def test_missing_markers_are_reported(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("no generated markers\n", encoding="utf-8")
    diagnostics = inventory.check(tmp_path)
    assert len(diagnostics) == 1
    assert "must contain exactly one" in diagnostics[0].reason
