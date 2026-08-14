from __future__ import annotations

from pathlib import Path

import pytest

from tools.repo_maintenance.scaffold import planned_outputs


def test_scaffold_plans_only_plugin_metadata(tmp_path: Path) -> None:
    config = tmp_path / "tools/maintenance/catalog.toml"
    config.parent.mkdir(parents=True)
    config.write_text("version = 1\n", encoding="utf-8")
    outputs = planned_outputs(tmp_path, "example-plugin", "Example maintenance workflows.")
    paths = {path.as_posix() for path in outputs}
    assert "plugins/example-plugin/.codex-plugin/plugin.json" in paths
    assert "plugins/example-plugin/ownership.json" in paths
    assert not any("/skills/" in path or path.endswith("/SKILL.md") for path in paths)
    assert not (tmp_path / "plugins/example-plugin").exists()


@pytest.mark.parametrize("name", ["Uppercase", "two--hyphens", "../escape", ""])
def test_scaffold_rejects_unsafe_names(tmp_path: Path, name: str) -> None:
    with pytest.raises(ValueError, match="plugin name"):
        planned_outputs(tmp_path, name, "Description")
