from __future__ import annotations

import copy
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tools.repo_maintenance.schemas import load_schema, load_yaml_text, schema_errors

CONFIG_ROOT = Path("plugins/internal-training-course/skills/course-wiki-migration-orchestrator")
CONFIG_NAMES = ("references/atrto-config.yaml", "references/course-config-template.yaml")
EXPECTED = {
    "course_title": "Adversary Tactics: Red Team Operations",
    "local_preview_url": "http://127.0.0.1:1313",
    "preview_url": "https://pr-1.d3i8gdc0r1f7xa.amplifyapp.com/",
    "commit_messages.stage1": "Set up scaffolding from wiki-course-atd-instructor",
    "commit_messages.stage2": "Import and convert ATRTO course content",
}


@pytest.mark.parametrize("relative_config", CONFIG_NAMES)
def test_real_course_config_schema(repo_root: Path, relative_config: str) -> None:
    schema = load_schema(repo_root, "course-config")
    value = load_yaml_text((repo_root / CONFIG_ROOT / relative_config).read_text(encoding="utf-8"))
    assert schema_errors(value, schema) == []


@pytest.mark.parametrize("relative_config", CONFIG_NAMES)
def test_real_cfg_get_helper(repo_root: Path, relative_config: str) -> None:
    helper = repo_root / CONFIG_ROOT / "scripts/common.sh"
    config = repo_root / CONFIG_ROOT / relative_config
    script = (
        'source "$1"; shift; config=$1; shift; for key in "$@"; do cfg_get "$config" "$key"; done'
    )
    env = os.environ.copy()
    env["PATH"] = f"{Path(sys.executable).parent}:{env['PATH']}"
    result = subprocess.run(
        ["bash", "-c", script, "bash", str(helper), str(config), *EXPECTED],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.stdout.splitlines() == list(EXPECTED.values())


@pytest.mark.parametrize(
    ("mutation", "field"),
    [
        (lambda value: value.pop("course_title"), "course_title"),
        (lambda value: value.__setitem__("target_repo", 42), "target_repo"),
        (lambda value: value.__setitem__("preview_url", "ftp://example.test"), "preview_url"),
        (lambda value: value["commit_messages"].__setitem__("stage1", "   "), "stage1"),
    ],
)
def test_invalid_course_config_is_rejected(repo_root: Path, mutation, field: str) -> None:
    schema = load_schema(repo_root, "course-config")
    base = load_yaml_text((repo_root / CONFIG_ROOT / CONFIG_NAMES[0]).read_text(encoding="utf-8"))
    value = copy.deepcopy(base)
    mutation(value)
    assert any(field in path or field in reason for path, reason in schema_errors(value, schema))
