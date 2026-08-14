from __future__ import annotations

import copy
from pathlib import Path

from tools.repo_maintenance.checks import check_policy
from tools.repo_maintenance.models import CheckContext
from tools.repo_maintenance.policy import public_recipes


def test_real_toolchain_and_recipe_policy_passes(repo_root: Path) -> None:
    assert check_policy.run(CheckContext(repo_root)) == []


def test_every_public_recipe_is_classified(repo_root: Path) -> None:
    policy = check_policy.load_toml_mapping(repo_root / "tools/maintenance/recipes.toml")
    declared = {item["name"] for item in policy["recipes"]}
    assert declared == public_recipes(repo_root)


def test_core_recipe_cannot_be_networked(repo_root: Path, monkeypatch) -> None:
    real_load = check_policy.load_toml_mapping

    def altered(path: Path):
        value = real_load(path)
        if path.name == "recipes.toml":
            value = copy.deepcopy(value)
            next(item for item in value["recipes"] if item["name"] == "check")["network"] = True
        return value

    monkeypatch.setattr(check_policy, "load_toml_mapping", altered)
    reasons = [item.reason for item in check_policy.run(CheckContext(repo_root))]
    assert any("must be offline/read-only" in reason for reason in reasons)


def test_devcontainer_uses_the_canonical_maintenance_versions(
    repo_root: Path, tmp_path: Path
) -> None:
    just_version = check_policy.toolchain(repo_root)["tools"]["just"]
    copy_root = tmp_path / "repo"
    devcontainer = copy_root / ".devcontainer/devcontainer.json"
    devcontainer.parent.mkdir(parents=True)
    source = repo_root / ".devcontainer/devcontainer.json"
    devcontainer.write_text(
        source.read_text(encoding="utf-8").replace(
            f"just --version {just_version}", "just --version 0.1.0"
        ),
        encoding="utf-8",
    )
    for relative in (
        "tools/maintenance/toolchain.toml",
        "tools/maintenance/recipes.toml",
        "tools/maintenance/pyproject.toml",
        ".github/workflows/quality.yml",
        ".github/workflows/scheduled-maintenance.yml",
        "justfile",
    ):
        destination = copy_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((repo_root / relative).read_bytes())
    source_just = repo_root / "tools/maintenance/just"
    destination_just = copy_root / "tools/maintenance/just"
    destination_just.mkdir(parents=True)
    for path in source_just.glob("*.just"):
        (destination_just / path.name).write_bytes(path.read_bytes())

    reasons = [item.reason for item in check_policy.run(CheckContext(copy_root))]

    expected = f"missing contributor setup pin 'just --version {just_version} --locked'"
    assert any(expected in reason for reason in reasons)
