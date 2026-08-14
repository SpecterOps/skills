from __future__ import annotations

import re
from typing import Any

from tools.repo_maintenance.models import CheckContext, CheckSpec, Diagnostic
from tools.repo_maintenance.policy import load_toml_mapping, public_recipes, toolchain
from tools.repo_maintenance.schemas import load_yaml_text

PINNED_DEPENDENCY = re.compile(r"^([A-Za-z0-9_.-]+)==(.+)$")
MUTATIONS = {"none", "local-cache", "declared-output", "maintenance-source"}


def _issue(path: str, reason: str) -> Diagnostic:
    return Diagnostic("maintenance.policy", path, reason)


def _dependency_versions(project: dict[str, Any]) -> dict[str, str]:
    values = list(project.get("project", {}).get("dependencies", []))
    values.extend(project.get("dependency-groups", {}).get("dev", []))
    result = {}
    for value in values:
        match = PINNED_DEPENDENCY.fullmatch(value)
        if match:
            result[match.group(1)] = match.group(2)
    return result


def run(context: CheckContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    toolchain_path = "tools/maintenance/toolchain.toml"
    recipes_path = "tools/maintenance/recipes.toml"
    try:
        pins = toolchain(context.root)
        recipes = load_toml_mapping(context.root / recipes_path)
        project = load_toml_mapping(context.root / "tools/maintenance/pyproject.toml")
        workflow = load_yaml_text(
            (context.root / ".github/workflows/quality.yml").read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as exc:
        return [_issue("tools/maintenance", str(exc))]

    if pins.get("version") != 1:
        diagnostics.append(_issue(toolchain_path, "version must equal 1"))
    python = pins.get("python", {})
    tools = pins.get("tools", {})
    actions = pins.get("actions", {})
    dependencies = pins.get("dependencies", {})
    if project.get("project", {}).get("requires-python") != python.get("requirement"):
        diagnostics.append(_issue(toolchain_path, "Python requirement differs from pyproject.toml"))
    if project.get("tool", {}).get("repo-maintenance", {}).get("uv-version") != tools.get("uv"):
        diagnostics.append(_issue(toolchain_path, "uv version differs from pyproject.toml"))
    actual_dependencies = _dependency_versions(project)
    for name, expected in dependencies.items() if isinstance(dependencies, dict) else ():
        if actual_dependencies.get(name) != expected:
            diagnostics.append(
                _issue(toolchain_path, f"dependency {name!r} is not pinned to {expected!r}")
            )

    workflow_texts = {
        path: (context.root / path).read_text(encoding="utf-8")
        for path in (
            ".github/workflows/quality.yml",
            ".github/workflows/scheduled-maintenance.yml",
        )
    }
    expected_fragments = (
        f'python-version: "{python.get("minor")}"',
        f"uv=={tools.get('uv')}",
        f"just --version {tools.get('just')} --locked",
        f"PSScriptAnalyzer -RequiredVersion {tools.get('psscriptanalyzer')}",
        f"actions/checkout@{actions.get('checkout')}",
        f"actions/setup-python@{actions.get('setup-python')}",
    )
    for path, workflow_text in workflow_texts.items():
        required = (
            tuple(item for item in expected_fragments if not item.startswith("PSScriptAnalyzer"))
            if path.endswith("scheduled-maintenance.yml")
            else expected_fragments
        )
        for fragment in required:
            if fragment not in workflow_text:
                diagnostics.append(_issue(path, f"missing pin {fragment!r}"))
    if not isinstance(workflow, dict):
        diagnostics.append(_issue(".github/workflows/quality.yml", "workflow must be a mapping"))

    declarations = recipes.get("recipes", []) if isinstance(recipes, dict) else []
    names = [item.get("name") for item in declarations if isinstance(item, dict)]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    for name in duplicates:
        diagnostics.append(_issue(recipes_path, f"duplicate recipe declaration {name!r}"))
    declared = {name for name in names if isinstance(name, str)}
    actual = public_recipes(context.root)
    for name in sorted(actual - declared):
        diagnostics.append(_issue(recipes_path, f"public recipe {name!r} is not classified"))
    for name in sorted(declared - actual):
        diagnostics.append(_issue(recipes_path, f"declares missing public recipe {name!r}"))
    for item in declarations:
        if not isinstance(item, dict):
            diagnostics.append(_issue(recipes_path, "recipe declarations must be mappings"))
            continue
        if not isinstance(item.get("network"), bool):
            diagnostics.append(
                _issue(recipes_path, f"recipe {item.get('name')!r} needs network=true/false")
            )
        if item.get("mutation") not in MUTATIONS:
            diagnostics.append(
                _issue(recipes_path, f"recipe {item.get('name')!r} has invalid mutation")
            )
        if item.get("name") in {"check", "ci", "test", "validate"} and (
            item.get("network") is not False or item.get("mutation") != "none"
        ):
            diagnostics.append(
                _issue(
                    recipes_path, f"core gate recipe {item.get('name')!r} must be offline/read-only"
                )
            )
    return diagnostics


CHECK = CheckSpec("maintenance.policy", frozenset({"policy", "core", "ci"}), run)
