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
    assert "plugins/example-plugin/.claude-plugin/plugin.json" in paths
    assert "plugins/example-plugin/ownership.json" in paths
    assert not any("/skills/" in path or path.endswith("/SKILL.md") for path in paths)
    assert not (tmp_path / "plugins/example-plugin").exists()
    ownership = outputs[Path("plugins/example-plugin/ownership.json")]
    assert '"support": "https://github.com/SpecterOps/skills/issues"' in ownership
    assert '"channel": "unreleased"' in ownership
    readme = outputs[Path("plugins/example-plugin/README.md")]
    for heading in (
        "## Status",
        "## Supported clients",
        "## Prerequisites",
        "## Skills",
        "## Example prompts",
        "## Development",
        "## Support",
        "## Release",
    ):
        assert heading in readme


def test_scaffold_can_omit_the_claude_manifest(tmp_path: Path) -> None:
    config = tmp_path / "tools/maintenance/catalog.toml"
    config.parent.mkdir(parents=True)
    config.write_text("version = 1\n", encoding="utf-8")

    outputs = planned_outputs(
        tmp_path,
        "example-plugin",
        "Example maintenance workflows.",
        manifests=("codex",),
    )

    assert Path("plugins/example-plugin/.codex-plugin/plugin.json") in outputs
    assert Path("plugins/example-plugin/.claude-plugin/plugin.json") not in outputs


@pytest.mark.parametrize("manifests", [("claude",), ("codex", "unknown")])
def test_scaffold_rejects_unsupported_manifest_selections(
    tmp_path: Path, manifests: tuple[str, ...]
) -> None:
    with pytest.raises(ValueError, match="manifest"):
        planned_outputs(tmp_path, "example-plugin", "Description", manifests=manifests)


@pytest.mark.parametrize("support_url", ["http://example.test/issues", "https:///missing-host"])
def test_scaffold_rejects_an_invalid_support_url(tmp_path: Path, support_url: str) -> None:
    with pytest.raises(ValueError, match="support URL"):
        planned_outputs(
            tmp_path,
            "example-plugin",
            "Description",
            support_url=support_url,
        )


@pytest.mark.parametrize("name", ["Uppercase", "two--hyphens", "../escape", ""])
def test_scaffold_rejects_unsafe_names(tmp_path: Path, name: str) -> None:
    with pytest.raises(ValueError, match="plugin name"):
        planned_outputs(tmp_path, name, "Description")
