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
