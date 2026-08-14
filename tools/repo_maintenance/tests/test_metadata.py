from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from tools.repo_maintenance.checks import check_metadata
from tools.repo_maintenance.models import CheckContext


def _fixture(tmp_path: Path) -> tuple[Path, Path, dict]:
    root = tmp_path
    skill = root / "plugins/demo/skills/example"
    (skill / "agents").mkdir(parents=True)
    (skill / "assets").mkdir()
    (skill / "assets/icon.svg").write_text("<svg/>", encoding="utf-8")
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Synthetic example skill.\n---\n",
        encoding="utf-8",
    )
    ui = {
        "interface": {
            "display_name": "Example",
            "short_description": "Perform the synthetic example workflow",
            "default_prompt": "Use $example for this workflow.",
            "icon_small": "./assets/icon.svg",
            "brand_color": "#123ABC",
        },
        "policy": {"allow_implicit_invocation": True},
        "dependencies": {"tools": [{"type": "mcp", "value": "synthetic"}]},
    }
    ui_path = skill / "agents/openai.yaml"
    ui_path.write_text(yaml.safe_dump(ui, sort_keys=False), encoding="utf-8")
    manifest_root = root / "plugins/demo/.codex-plugin"
    manifest_root.mkdir()
    manifest = {
        "name": "demo",
        "skills": "./skills/",
        "interface": {
            "defaultPrompt": ["One", "Two", "Three"],
            "composerIcon": "./skills/example/assets/icon.svg",
            "logo": "./skills/example/assets/icon.svg",
        },
    }
    (manifest_root / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "agents").mkdir()
    return root, ui_path, ui


def _write_ui(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (lambda ui: ui["interface"].__setitem__("short_description", "too short"), "25-64"),
        (
            lambda ui: ui["interface"].__setitem__(
                "short_description", "This description was visibly truncated..."
            ),
            "truncation suffix",
        ),
        (
            lambda ui: ui["interface"].__setitem__("default_prompt", "Use another skill."),
            "$example",
        ),
        (lambda ui: ui["interface"].__setitem__("brand_color", "blue"), "six-digit"),
        (lambda ui: ui["interface"].__setitem__("icon_small", "../escape.svg"), "escapes"),
        (lambda ui: ui["policy"].__setitem__("allow_implicit_invocation", "yes"), "boolean"),
        (lambda ui: ui["dependencies"].__setitem__("tools", [{"type": "http"}]), "MCP"),
    ],
)
def test_skill_ui_semantic_failures(tmp_path: Path, mutation, reason: str) -> None:
    root, path, base = _fixture(tmp_path)
    value = copy.deepcopy(base)
    mutation(value)
    _write_ui(path, value)
    assert any(reason in item.reason for item in check_metadata.run(CheckContext(root)))


def test_plugin_prompt_limit_is_enforced(tmp_path: Path) -> None:
    root, _, _ = _fixture(tmp_path)
    manifest = root / "plugins/demo/.codex-plugin/plugin.json"
    value = json.loads(manifest.read_text())
    value["interface"]["defaultPrompt"].append("Four")
    manifest.write_text(json.dumps(value), encoding="utf-8")
    assert any("maximum is 3" in item.reason for item in check_metadata.run(CheckContext(root)))


def test_malformed_plugin_and_agent_metadata_are_reported(tmp_path: Path) -> None:
    root, _, _ = _fixture(tmp_path)
    manifest = root / "plugins/demo/.codex-plugin/plugin.json"
    manifest.write_text("[", encoding="utf-8")
    agent = root / "agents/broken.toml"
    agent.write_text('name = "unterminated', encoding="utf-8")

    diagnostics = check_metadata.run(CheckContext(root))

    assert {item.path for item in diagnostics} == {
        "agents/broken.toml",
        "plugins/demo/.codex-plugin/plugin.json",
    }


def test_real_repository_metadata_contracts_pass(repo_root: Path) -> None:
    assert check_metadata.run(CheckContext(repo_root)) == []
