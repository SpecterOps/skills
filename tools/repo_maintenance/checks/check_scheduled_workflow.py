from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.repo_maintenance.checks.check_workflows import ACTION_PIN
from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.schemas import load_yaml_text

EXPECTED_COMMANDS = {
    "just check-external-links",
    "just check-upstream-bloodhound",
}
FORBIDDEN_COMMANDS = ("git push", "gh api", "gh release", "curl ", "wget ")


def validate(
    value: Any, path: str = ".github/workflows/scheduled-maintenance.yml"
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    def issue(reason: str) -> None:
        diagnostics.append(Diagnostic("workflows.scheduled", path, reason))

    if not isinstance(value, dict):
        return [Diagnostic("workflows.scheduled", path, "workflow must be a mapping")]
    if value.get("permissions") != {"contents": "read"}:
        issue("permissions must be exactly contents: read")
    triggers = value.get("on", value.get(True))
    if not isinstance(triggers, dict) or set(triggers) != {"schedule", "workflow_dispatch"}:
        issue("triggers must be exactly schedule and workflow_dispatch")
    jobs = value.get("jobs")
    if not isinstance(jobs, dict) or set(jobs) != {"network-audit"}:
        issue("workflow must contain only the network-audit job")
        return diagnostics
    job = jobs["network-audit"]
    if not isinstance(job, dict):
        issue("network-audit job must be a mapping")
        return diagnostics
    if job.get("permissions") not in (None, {"contents": "read"}):
        issue("job permissions must be exactly contents: read")
    if job.get("continue-on-error") not in (None, False):
        issue("job must not continue on error")
    timeout = job.get("timeout-minutes")
    if not isinstance(timeout, int) or timeout <= 0:
        issue("job requires a positive timeout-minutes")
    commands = set()
    steps = job.get("steps")
    if not isinstance(steps, list):
        issue("job steps must be a list")
        return diagnostics
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            issue(f"step {index} must be a mapping")
            continue
        uses = step.get("uses")
        if isinstance(uses, str) and not ACTION_PIN.fullmatch(uses):
            issue(f"action {uses!r} is not pinned to a full commit SHA")
        if isinstance(uses, str) and uses.startswith("actions/checkout@"):
            settings = step.get("with")
            if not isinstance(settings, dict) or settings.get("persist-credentials") is not False:
                issue("checkout must set persist-credentials: false")
        if step.get("continue-on-error") not in (None, False):
            issue(f"step {index} must not continue on error")
        command = step.get("run")
        if isinstance(command, str):
            commands.update(line.strip() for line in command.splitlines())
            for forbidden in FORBIDDEN_COMMANDS:
                if forbidden in command.lower():
                    issue(f"workflow invokes forbidden command fragment {forbidden!r}")
    missing = sorted(EXPECTED_COMMANDS - commands)
    if missing:
        issue("workflow is missing commands: " + ", ".join(missing))
    return diagnostics


def run(context: CheckContext) -> list[Diagnostic]:
    relative = Path(".github/workflows/scheduled-maintenance.yml")
    try:
        value = load_yaml_text((context.root / relative).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [Diagnostic("workflows.scheduled", relative.as_posix(), str(exc))]
    return validate(value, relative.as_posix())


CHECK = CheckSpec("workflows.scheduled", frozenset({"workflows", "ci"}), run)
