---
name: course-wiki-migration-orchestrator
description: "Coordinate staged course wiki migrations as a reusable sub-agent workflow. Use when a user wants one orchestrator to run stage 1 scaffold creation, stage 2 content migration, local or deployed browser verification, git commit/push steps, and the stage 3 QA plus targeted-polish pass by calling the stage skills and helper scripts with a per-course config file."
---

# Course Wiki Migration Orchestrator

Use this skill inside a spawned worker sub-agent when the user wants the course wiki migration process operationalized end-to-end. This orchestrator does not replace the stage skills. It sequences them, loads the course config, uses helper scripts for deterministic operations, and hands content-aware work to the stage skills.

Load these resources as needed:
- [references/orchestrator-workflow.md](references/orchestrator-workflow.md) for stage sequencing, stop conditions, and handoff rules.
- [references/course-config-template.yaml](references/course-config-template.yaml) for the course config schema.
- [references/atrto-config.yaml](references/atrto-config.yaml) for the first working course config example using the shared template scaffold.
- `scripts/*.sh` for config validation, local preview startup, and git helpers.

## Inputs To Confirm From The Environment

- Course config path.
- Requested stage scope: `stage1`, `stage2`, `stage3`, or `all`.
- QA mode: `local`, `deployed`, or `both`.
- Whether the user wants the orchestrator to auto-commit and auto-push.
- Preview URL if deployed QA is requested and the config does not already contain one.

Default assumptions:
- This orchestrator is used in a spawned worker sub-agent.
- The orchestrator may call `course-wiki-stage1-scaffold`, `course-wiki-stage2-content-migration`, and `course-wiki-stage3-qa`.
- The orchestrator may use Playwright MCP for browser verification.
- The orchestrator may use helper scripts for config loading, local preview startup, and git actions.

## Workflow

## 1. Preflight

- Read the course config and validate required fields with `scripts/common.sh`.
- Confirm source paths, target repo path, and current git branch/repo state.
- If the config is incomplete, stop and report the missing keys before any edits.
- If the user asked for deployed QA and no preview URL is available, request it after push and before browser checks.
- Before local build or preview steps, ensure a compatible Hugo binary is available.
  - Prefer `HUGO_BIN` when set.
  - Otherwise prefer `/tmp/course-tools/hugo/hugo` when present.
  - Fall back to `hugo` on PATH only when compatible with the theme.

## 2. Stage Routing

- If the user asked for `stage1`, load `course-wiki-stage1-scaffold` and complete stage 1 only.
- If the user asked for `stage2`, assume the scaffold already exists, load `course-wiki-stage2-content-migration`, and complete stage 2 only.
- If the user asked for `stage3`, load `course-wiki-stage3-qa` and run the stage-3 QA plus targeted-polish pass only.
- If the user asked for `all`, run stage 1, then stage 2, then the stage-3 QA plus targeted-polish pass in order.

## 3. Use Helper Scripts For Deterministic Operations

- Use `scripts/run_stage1.sh` for stage-1 config preflight, scaffold sanity checks, local preview startup, and git automation support.
- Use `scripts/run_stage2.sh` for stage-2 config preflight, legacy-source Git LFS hydration, LFS pointer checks, local build checks, and git automation support.
- Use `scripts/run_stage3_stub.sh` for the stage-3 QA contract, route-sweep expectations, and result formatting.
- Use `scripts/start_local_preview.sh` when QA mode includes `local`.

These scripts support the stage skills. They do not replace content-aware edits or migration decisions.

## 4. Sub-Agent Behavior

- Treat the orchestrator as the stage-sequencing sub-agent.
- Keep the main thread informed of stage boundaries, local build results, deploy/push status, and browser findings.
- If the user explicitly wants parallel work, the orchestrator may spawn bounded workers for non-overlapping tasks. Otherwise keep execution sequential.
- Do not blur stage boundaries:
  - finish stage 1 before stage 2
  - finish stage 2 before stage 3 QA

## 5. Git And QA Rules

- If auto-commit/auto-push is requested, ensure checks pass before committing.
- Use the commit messages from the course config when present.
- For `local` QA, start the local Hugo preview and verify it with Playwright.
- For `deployed` QA, use the supplied preview URL after push. If preview authentication is enabled, look for credentials in the target course README before treating the deploy as inaccessible.
- For `both`, run local QA first, then deployed QA.
- Treat local build success as necessary but insufficient. Stage 3 must also include build-output sanity checks for leaked Hextra markup, representative UI checks such as dark mode and sidebar behavior, and at least one explicit long-code-block rendering check.

## 6. Stop Conditions

- Stage 1 stops after scaffold creation, local validation, optional push, and requested QA.
- Stage 2 stops after content migration, local validation, optional push, and requested QA.
- Stage 3 currently stops after QA, one bounded rendering-only polish pass, and post-fix validation. It does not attempt unlimited fix loops.

## Reference

- Use [references/orchestrator-workflow.md](references/orchestrator-workflow.md) as the operating contract for stage order, inputs, and QA mode behavior.
