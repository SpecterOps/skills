from __future__ import annotations

import copy
from pathlib import Path

import pytest

from tools.repo_maintenance.checks.check_workflows import validate
from tools.repo_maintenance.schemas import load_yaml_text


@pytest.fixture
def workflow(repo_root: Path):
    path = repo_root / ".github/workflows/quality.yml"
    return load_yaml_text(path.read_text(encoding="utf-8"))


def _reasons(value) -> list[str]:
    return [diagnostic.reason for diagnostic in validate(value)]


def test_real_quality_workflow_satisfies_policy(workflow) -> None:
    assert validate(workflow) == []


def test_unpinned_action_is_rejected(workflow) -> None:
    value = copy.deepcopy(workflow)
    value["jobs"]["linux-quality"]["steps"][0]["uses"] = "actions/checkout@v4"
    assert any("full commit SHA" in reason for reason in _reasons(value))


def test_write_permission_and_persisted_credentials_are_rejected(workflow) -> None:
    value = copy.deepcopy(workflow)
    value["permissions"] = {"contents": "write"}
    value["jobs"]["linux-quality"]["steps"][0]["with"]["persist-credentials"] = True
    reasons = _reasons(value)
    assert any("permissions" in reason for reason in reasons)
    assert any("persist-credentials" in reason for reason in reasons)


@pytest.mark.parametrize(
    "command",
    [
        "just generate-catalog",
        "just refresh-bloodhound",
        "just check-external-links",
        "just check-upstream-bloodhound",
        "python report.py --include-sensitive",
    ],
)
def test_mutating_networked_and_sensitive_commands_are_rejected(workflow, command: str) -> None:
    value = copy.deepcopy(workflow)
    value["jobs"]["linux-quality"]["steps"].append({"run": command})
    assert any("forbidden command" in reason for reason in _reasons(value))


def test_uploads_and_missing_timeouts_are_rejected(workflow) -> None:
    value = copy.deepcopy(workflow)
    value["jobs"]["linux-quality"].pop("timeout-minutes")
    value["jobs"]["linux-quality"]["steps"].append({"uses": "actions/upload-artifact@" + "a" * 40})
    reasons = _reasons(value)
    assert any("timeout-minutes" in reason for reason in reasons)
    assert any("must not upload artifacts" in reason for reason in reasons)


def test_schedule_and_nondefault_push_branch_are_rejected(workflow) -> None:
    value = copy.deepcopy(workflow)
    triggers = value.get("on", value.get(True))
    triggers["schedule"] = [{"cron": "0 0 * * *"}]
    triggers["push"] = {"branches": ["*"]}
    reasons = _reasons(value)
    assert any("triggers" in reason for reason in reasons)
    assert any("default master branch" in reason for reason in reasons)
