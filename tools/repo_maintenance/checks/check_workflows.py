from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_yaml_text

ACTION_PIN = re.compile(r"^[^\s@]+@[0-9a-f]{40}$")
FORBIDDEN_RUN = (
    "--include-sensitive",
    "refresh-",
    "generate-",
    "check-external",
    "check-upstream",
)


def validate(value: Any, path: str = ".github/workflows/quality.yml") -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    def issue(reason: str) -> None:
        diagnostics.append(Diagnostic("workflows.policy", path, reason))

    if not isinstance(value, dict):
        return [Diagnostic("workflows.policy", path, "workflow must be a mapping")]
    permissions = value.get("permissions")
    if permissions != {"contents": "read"}:
        issue("top-level permissions must be exactly contents: read")
    triggers = value.get("on", value.get(True))
    if not isinstance(triggers, dict):
        issue("quality workflow triggers must be exactly pull_request and push")
    else:
        if set(triggers) != {"pull_request", "push"}:
            issue("quality workflow triggers must be exactly pull_request and push")
        if triggers.get("push") != {"branches": ["master"]}:
            issue("push trigger must be restricted to the default master branch")
    environment = value.get("env")
    if not isinstance(environment, dict) or environment.get("MAINTENANCE_PYTHON") != "python":
        issue("workflow must select the setup-python interpreter through MAINTENANCE_PYTHON")
    concurrency = value.get("concurrency")
    if not isinstance(concurrency, dict) or concurrency.get("cancel-in-progress") is not True:
        issue("workflow must cancel superseded runs")
    jobs = value.get("jobs")
    if not isinstance(jobs, dict):
        issue("workflow jobs must be a mapping")
        return diagnostics
    expected_runners = {"linux-quality": "ubuntu-24.04", "windows-powershell": "windows-2025"}
    for job_name, runner in expected_runners.items():
        if not isinstance(jobs.get(job_name), dict) or jobs[job_name].get("runs-on") != runner:
            issue(f"job {job_name!r} must run on {runner}")
    run_commands: list[str] = []
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            issue(f"job {job_name!r} must be a mapping")
            continue
        timeout = job.get("timeout-minutes")
        if not isinstance(timeout, int) or timeout <= 0:
            issue(f"job {job_name!r} requires a positive timeout-minutes")
        job_permissions = job.get("permissions")
        if isinstance(job_permissions, dict) and any(
            value == "write" for value in job_permissions.values()
        ):
            issue(f"job {job_name!r} grants write permission")
        steps = job.get("steps")
        if not isinstance(steps, list):
            issue(f"job {job_name!r} steps must be a list")
            continue
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                issue(f"job {job_name!r} step {index} must be a mapping")
                continue
            uses = step.get("uses")
            if isinstance(uses, str):
                if not ACTION_PIN.fullmatch(uses):
                    issue(f"action {uses!r} is not pinned to a full commit SHA")
                if uses.startswith("actions/upload-artifact@"):
                    issue("core workflow must not upload artifacts")
                if uses.startswith("actions/checkout@"):
                    settings = step.get("with")
                    if (
                        not isinstance(settings, dict)
                        or settings.get("persist-credentials") is not False
                    ):
                        issue("checkout must set persist-credentials: false")
            command = step.get("run")
            if isinstance(command, str):
                run_commands.append(command)
                for forbidden in FORBIDDEN_RUN:
                    if forbidden in command:
                        issue(f"core workflow invokes forbidden command fragment {forbidden!r}")
            if step.get("continue-on-error") is True:
                issue(f"job {job_name!r} step {index} must not continue on error")
    combined = "\n".join(run_commands)
    for required in (
        "uv==0.12.3",
        "just --version 1.51.0 --locked",
        "uv sync --project tools/maintenance --locked",
        "just ci",
        "Install-Module PSScriptAnalyzer -RequiredVersion 1.24.0",
        "just check-powershell",
    ):
        if required not in combined:
            issue(f"workflow is missing required pinned command: {required}")
    return diagnostics


def run(context: CheckContext) -> list[Diagnostic]:
    relative = Path(".github/workflows/quality.yml")
    path = context.root / relative
    try:
        value = load_yaml_text(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [Diagnostic("workflows.policy", relative.as_posix(), str(exc))]
    return validate(value, relative.as_posix())


CHECK = CheckSpec("workflows.policy", frozenset({"workflows", "ci"}), run)
