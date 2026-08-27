---
name: bhe-change-delivery
description: Implement, validate, review, and deliver BloodHound Enterprise and BHCE code changes from authoritative intent through BHE/BHCE parity, enterprise review, commits, pull-request preparation, rebases, CI diagnosis, and follow-through. Use for product-changing BHE work; route local stack ownership to `bhe-dev-environment` and review-only judgment to `bhe-enterprise-review`.
---

# BHE Change Delivery

Own the product change and its evidence from agreed intent through PR follow-through. Use `bhe-dev-environment` for worktrees and runtime state, `bhe-ui-playwright` for browser-visible validation, `bhe-sample-data-ingest` for standard-stack data, and `bhe-enterprise-review` for the immutable review gate.

## Preserve Task Identity

For code-changing tasks, preserve the existing Codex task title text exactly and manage only a trailing net-line-count suffix in the form ` (+N)`. At meaningful handoffs, replace an existing trailing ` (+integer)` suffix with the current value, or append ` (+N)` when no such suffix exists. Never change any other title text. Calculate `N` only from files intended for the product PR: additions minus deletions across applicable BHE/BHCE repositories. Exclude standalone Playwright harnesses, local validation tooling, generated artifacts, and other non-PR files. Omit the suffix for read-only work.

## Route Supporting Work

- Invoke `bhe-dev-environment` before creating or selecting a worktree, operating Docker, diagnosing local startup, or releasing task-owned runtime resources.
- Invoke `bhe-enterprise-review` after implementation and focused validation stabilize and before preparing the PR proposal.
- Invoke `bhe-ui-playwright` for browser-visible work and record whether durable coverage is committed, already exists, is standalone-only, or is unnecessary.
- Invoke `bhe-sample-data-ingest` when a standard stack needs official AD or Entra data.
- When the private `bloodhound` plugin is installed, use its domain skills for Cypher, AD/ADCS, Entra/Azure, OpenGraph, or OpenHound semantics. Those skills supplement rather than replace BHE/BHCE parity, repository tests, enterprise review, accessibility validation, or PR approval gates.

Read [bhe-bhce-parity.md](references/bhe-bhce-parity.md) for every meaningful behavior or contract change. Read [pr-readiness.md](references/pr-readiness.md) before committing, preparing, creating, updating, rebasing, or monitoring a PR. Do not preload both references for unrelated work.

## Resolve Intent and Scope

Use the Jira ticket when available as the source for the problem, intended outcome, acceptance criteria, constraints, exclusions, and planned verification. When direct Jira access is unavailable, use user-provided text and the agreed task scope without inventing missing decisions.

Before editing:

1. Confirm the worktree and branch belong to this task.
2. Establish a passing focused baseline where practical.
3. Inspect repository instructions and the corresponding BHE/BHCE surface.
4. Identify which evidence will demonstrate each observable acceptance criterion.
5. Separate product work from local harnesses, generated artifacts, and unrelated existing changes.

Use a fresh production-baseline worktree for new PR-bound work unless the user explicitly selected an existing worktree or branch.

## Orchestrate Independent Lanes

When sub-agents are available, proactively delegate in-scope work that can proceed independently and would materially reduce elapsed time or improve independent judgment. The user's request to complete the product change is sufficient authorization for this internal delegation unless the user says not to delegate; it does not authorize broader scope or additional external mutations. Do not wait for a separate invitation to delegate useful investigation, non-overlapping implementation, focused validation, or review work, and do not block progress merely waiting for an agent slot.

Keep the primary agent accountable for integration, cross-repository decisions, final verification, approval requests, and all remote mutations. Partition implementation by non-overlapping files, packages, repositories, or operational surfaces. Give each delegate the raw authoritative intent, exact worktree and branch, BHE/BHCE scope, validation expectations, and exclusive ownership. Require changed files, commands and tests, failures, assumptions, and remaining risks in the handoff.

Use these ownership lanes:

- Assign at most one `bhe-dev-environment` operator for the task-owned stack. That same lane owns `bhe-sample-data-ingest`; do not run ingest concurrently from another agent.
- Assign at most one `bhe-ui-playwright` browser-validation agent after the environment operator reports a stable target. The browser agent must not mutate stack state.
- Invoke `bhe-enterprise-review` in a fresh, independent review context for the immutable committed candidate. Supply raw intent and pinned SHAs, not author reasoning or a desired verdict.
- Delegate investigation and implementation only across non-overlapping ownership boundaries; sequence tightly coupled edits and integration work.

Do not delegate merely to increase agent count. Never allow a delegate to create or update a remote PR, accept external agreements, perform destructive resets, or operate another task's environment.

## Track BHE/BHCE Compatibility

For each meaningful change, inspect the corresponding BHCE surface and record one disposition:

`matched`, `equivalent`, `bhe-only`, `intentionally-divergent`, `deferred`, or `investigate`.

Initialize one task-owned ledger after selecting the worktree:

```bash
PARITY_LOG="<directory containing this SKILL.md>/scripts/bhe-parity-log.sh"
"$PARITY_LOG" init --task <task-slug> --repo <absolute-worktree-path>
```

Use `check --stage iteration` during development and `check --stage pr` before PR handoff. An unresolved investigation, pending validation, missing required reference, or deferred item without a concrete follow-up blocks readiness. Skip the ledger only for purely mechanical changes with no behavioral or compatibility implication.

## Validate Code Changes

- Make narrow, recoverable changes and run the smallest relevant validation after each iteration.
- For frontend work, treat Doodle UI as the default component and token system. Inspect existing Doodle components, compositions, tokens, and established usage before creating a component or dependency; reuse the closest clean fit and preserve accessibility behavior.
- Treat Material UI (MUI) as a legacy exception. If no viable Doodle path exists and the change would add or expand MUI, pause before implementation and warn with `MUI exception:` followed by the requirement, alternatives checked, why they do not fit, the smallest proposed MUI scope, and any migration follow-up.
- When editing an existing MUI surface, prefer an in-scope Doodle replacement when safe and proportionate; otherwise avoid expanding MUI. Do not turn focused work into an unrequested migration.
- Track reviewable changed lines during implementation, aim for at most 400, and follow the Reviewability Gate in [pr-readiness.md](references/pr-readiness.md) before a cohesive change grows beyond it.
- Target WCAG 2.2 Level AA for browser-visible work unless the repository specifies another AA version. Report known failures and unverified areas; do not claim conformance without evidence.
- Run relevant BHE tests for BHE-only code.
- Test both products for shared packages, APIs, schemas, generated clients, and shared contracts.
- Test BHCE plus the BHE consumer when changing `bhce/`.

## Diagnose CI and Intermittent Failures from Evidence

Do not propose a CI or flaky-test fix without the actual failed command, exception or error message, and relevant trace or job-log context. If logs are unavailable after two focused retrieval attempts, ask for the exact failure instead of guessing.

Before deep investigation, check cheap exits: the issue is already fixed, an open PR already addresses it, the failure is deterministic rather than intermittent, or many unrelated jobs show a shared infrastructure failure. Treat an existing diagnosis as a hypothesis and re-derive it from current evidence.

Classify the failure before editing: deterministic regression, test ordering or shared state, timing or race, resource exhaustion, external dependency, environment/configuration, or unrelated baseline failure. Local reproduction is useful for observing the mechanism; it does not replace required repository validation or terminal CI for a CI-only failure. Limit repeated local attempts per unchanged hypothesis to two.

Fix the identified source rather than skipping the test or weakening the assertion. Search the same file and relevant suite for sibling occurrences of the unsafe pattern. Keep unrelated CI failures out of the change and report them separately.

## Run the Enterprise Review Gate

After implementation and focused validation stabilize, invoke `bhe-enterprise-review` in a fresh independent sub-agent context on a clean immutable committed candidate whenever sub-agents are available. Provide the exact repository/worktree, live target ref, pinned target, merge-base and head SHAs, raw intent and acceptance criteria, BHE/BHCE scope, and sister-repository SHA when applicable. Do not prime the reviewer with implementation reasoning, expected findings, or a desired verdict. If independent delegation is unavailable, perform and disclose a self-review rather than skipping the gate.

Independently verify findings before acting. Fix valid blocking and important findings, rerun affected validation, and obtain a new receipt for the resulting exact head. A product-code change after `PASS` invalidates the receipt. Do not prepare a PR proposal while blocking or important findings remain, an unresolved decision exists, or the receipt is absent, stale, or non-`PASS`.

## Preflight PR Context

Before writing a PR proposal, run the deterministic context helper once and reuse its result:

```bash
BHE_DELIVERY_SKILL_DIR="<directory containing this SKILL.md>"
"$BHE_DELIVERY_SKILL_DIR/scripts/check-pr-context.sh"
```

Confirm the repository, visibility, current branch, upstream, push state, and default branch. Compare `git diff <merge-base>...HEAD --stat` and the complete diff with the agreed intent. Stop on unexpected files until the user confirms they belong or the change is separated.

For public repositories, inspect the title, body, branch name, commit messages, comments, screenshots, and diff for internal URLs, identifiers, customer data, private project names, or internal process details. Warn that the material will be public and obtain explicit confirmation immediately before creation.

Then follow [pr-readiness.md](references/pr-readiness.md) for Jira/template completeness, trust-package evidence, reviewability, parity, commits, approval, rebases, PR mutation, and monitoring.

## Approval and Follow-Through

Never create or mutate a remote PR, push to an open PR, rebase or force-push its branch, or rerun/cancel remote checks without the approval required by [pr-readiness.md](references/pr-readiness.md). An earlier rejection or request to wait remains a hard stop until the user explicitly changes direction.

After an approved PR mutation, verify GitHub attached the expected head and inspect only relevant failed jobs. Treat automated review comments as hypotheses and verify them against the code. Once expected CI and review feedback are terminal for the final head, route safe runtime release to `bhe-dev-environment`; do not delete volumes or task state as part of normal follow-through.
