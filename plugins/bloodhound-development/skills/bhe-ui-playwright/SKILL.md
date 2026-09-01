---
name: bhe-ui-playwright
description: Validate BloodHound Enterprise (BHE) and BHCE frontend changes with Playwright against task-owned local or isolated stacks, and decide whether durable repository-owned Playwright coverage belongs in the product PR. Use for UI features, browser regressions, interaction testing, accessibility coverage, real API-backed end-to-end scenarios, WebGL/ReGraph controls, or repeated frontend iteration.
---

# BHE UI Playwright

Validate frontend work in a real browser and deliberately choose between repository-owned regression coverage and standalone task-local validation. A ticket does not need to prescribe Playwright; infer the appropriate test layer from the behavior and regression risk.

## Delegated Browser-Validation Lane

This skill is designed to run as one focused browser-validation lane under `bhe-change-delivery` when it can overlap other independent work or provide cleaner validation ownership. Assign at most one browser agent to a task-owned target. Start only after the `bhe-dev-environment` operator reports a stable URL, credentials, and stack identity. The browser agent owns Playwright, screenshots, traces, browser-console evidence, and its validation handoff, but must not start, stop, seed, reset, or otherwise mutate the stack. Route stack changes back to the environment operator.

When this skill is used standalone or no useful parallel work exists, perform validation directly without spawning another agent.

## Establish the Target

1. Use `bhe-dev-environment` to identify the task-owned worktree, stack slug, URL, and credentials.
2. Verify the URL resolves only to `localhost`, `127.0.0.1`, or `*.localhost` before sending local credentials.
3. Verify the UI endpoint returns successfully.
4. Never reuse or restart another task's stack merely because it is available.

## Select the Harness

Use an existing Playwright setup in the owning product repository for committed regression coverage. Use a standalone harness outside the worktree for exploratory validation, real-backend scenarios not supported by the repository suite, or behavior that should not become a maintained product test. Do not add a second Playwright framework when a supported repository harness already exists.

Default standalone harness location:

```text
$HOME/Documents/codex/experiments/bhe-playwright-pilot
```

Override it with `BHE_PLAYWRIGHT_HARNESS` when needed. If no harness exists, create one outside the product repository with `@playwright/test`, a Chromium project, retained failure traces/screenshots/video, and environment-driven `BHE_URL`, `BHE_USERNAME`, and `BHE_PASSWORD`. Request approval before downloading packages or browsers.

## Decide Regression Coverage

At the start of each browser-visible task, record one disposition with a one-sentence rationale and revisit it if implementation changes the risk:

- `committed-playwright`: add or extend a repository-owned spec;
- `existing-playwright-coverage`: identify the committed scenario that already protects the behavior;
- `standalone-playwright-only`: validate in a task-local harness without adding product test code;
- `no-playwright`: explain why focused unit, static, API, or backend tests are sufficient.

Choose `committed-playwright` when the change introduces or alters a stable user workflow; fixes a browser-only or prior regression; changes routing, authentication, focus, forms, menus, dialogs, uploads, destructive actions, or multi-component behavior; adds or fixes accessibility semantics; or has meaningful empty, populated, loading, error, theme, permission, or browser states that unit tests do not adequately protect.

Usually choose another disposition for backend-only work, behavior-preserving refactors, small visual adjustments, unstable or temporary scenarios, behavior already covered by a durable spec, or canvas/WebGL internals that Playwright cannot observe reliably. Test graph transformations and aggregation rules with unit tests and use Playwright for observable surrounding controls.

Treat current validation and durable coverage as separate decisions. A browser-visible change may need standalone real-stack validation even when a committed mocked regression test is appropriate, and exploratory validation does not automatically belong in the product suite.

### Package Tests With the Change

Include focused committed Playwright coverage in the implementation PR by default so behavior and regression protection land atomically. Use a separate PR only for broad coverage backfills, shared test infrastructure needed by multiple changes, intentionally failing diagnostic baselines, or test work large enough to obscure the production change. Link split PRs reciprocally, state merge order, and do not leave required coverage as an undocumented follow-up.

## Iteration Workflow

1. When the selected disposition uses Playwright, establish the Playwright baseline before changing product code. Require it to pass unless an explicitly diagnostic or coverage-baselining ticket permits known failures.
2. Record the Playwright disposition and the behavior or risk it covers.
3. Make the smallest feature change and its focused unit tests.
4. For `committed-playwright`, add or extend the smallest meaningful repository scenario; for `standalone-playwright-only`, extend the external scenario only for behavior introduced in that iteration.
5. Run focused unit, type, lint, and formatting checks.
6. Run the targeted repository spec and task-owned-stack Playwright validation when applicable to the selected disposition.
7. Before PR handoff, run the full repository suite when the ticket, repository instructions, or regression scope requires it.
8. Verify the endpoint remains healthy and inspect browser errors.
9. Report cumulative line counts and the final disposition before handing control back to the user.

Do not commit, push, or prepare a PR unless the user separately requests it.

## Report Criterion-to-Evidence Results

At each meaningful handoff, connect validation to the behavior it is intended to prove. Report:

- the acceptance criterion, user-visible behavior, or regression risk;
- the repository or standalone scenario that exercises it;
- the exact command and observed result;
- relevant screenshot, trace, video, console, network, or accessibility evidence;
- whether the evidence is CI-enforced, manually executed, or exploratory;
- any state, browser, permission, theme, responsive condition, canvas behavior, or accessibility property that remains unverified.

Do not substitute a test name, screenshot, or statement that Playwright passed for an explanation of what the evidence demonstrates. When implementation changes invalidate earlier evidence, rerun the affected scenario before handoff.

## Write Reliable Scenarios

- Prefer role, label, placeholder, and test-id locators over CSS or DOM structure.
- Assert the initial control state before interacting.
- Await the specific API response for workflows that depend on real data.
- Avoid fixed sleeps; wait for visible state, URL changes, responses, or enabled controls.
- Capture `pageerror` events and fail with their messages.
- Capture failed requests and unexpected HTTP 4xx/5xx responses caused by the exercised flow. Document intentional failures such as negative-test responses instead of silently ignoring them.
- Keep one worker for shared local environments unless tests are demonstrably isolated.
- Retain automated diagnostic screenshots, video, and traces only on failure. Separately capture intentional reviewer screenshots for every browser-visible change that will be pushed in a PR.
- Test graph data transformations and aggregation rules with unit tests. WebGL/canvas output is not fully observable through DOM assertions.
- Keep committed scenarios narrow, deterministic, and aligned with repository fixtures. Mock only the APIs needed to establish the state under test; use standalone validation for complementary real-backend evidence.
- Report whether the repository suite is CI-enforced or manually executed. Never infer that green general UI checks ran a separately invoked Playwright suite.

## Optional Lighthouse Diagnostics

Run an authenticated Lighthouse audit when a change materially affects navigation, rendering, layout, bundles, or performance, or when the user requests it. Reuse the task-owned local URL and authenticate without persisting credentials. Report performance, accessibility, best-practice, and relevant web-vitals findings as diagnostics. Do not make a Lighthouse score a release gate unless the repository defines a budget, and do not treat Lighthouse accessibility results as a substitute for the interaction-focused WCAG checks below.

## WCAG AA Accessibility Gate

Target WCAG 2.2 Level AA for BHE browser-visible changes unless the repository documents a different WCAG AA version. At each iteration, apply the checks relevant to the changed surface:

- operate new controls with the keyboard and verify logical focus order and visible focus;
- verify accessible names, roles, values, expanded/selected/pressed states, and status announcements;
- verify text and meaningful UI-component contrast, zoom/reflow behavior, and that color is not the only cue;
- verify labels, instructions, error identification, and target size where the feature introduces them;
- prefer automated accessibility scanning when the existing harness already supports it, but never treat a clean scan as sufficient without interaction-focused manual checks.

For ReGraph/WebGL/canvas experiences, validate all surrounding DOM controls and keyboard paths. Explicitly report graph content or canvas interactions that cannot be verified through the accessibility tree as manual-check items rather than claiming conformance.

Warn the user immediately when a check fails or remains materially uncertain. Include the evidence, likely WCAG criterion or affected behavior, user impact, and recommended fix. Before PR preparation or submission, provide a concise accessibility recap of checks passed, automated findings, manual checks, unresolved risks, and proposed resolutions; clearly identify any issue that should block the PR.

Run the harness without printing or persisting the password:

```bash
BHE_UI_SKILL_DIR="<directory containing this SKILL.md>"
BHE_PASSWORD='<local-password>' \
  "$BHE_UI_SKILL_DIR/scripts/run-local.sh" \
  http://<task-slug>.bhe.localhost:<port>
```

The helper refuses non-local URLs. Set `BHE_USERNAME` only when it differs from `admin@example.com`.

## Report Lines at Every Iteration

Run:

```bash
BHE_UI_SKILL_DIR="<directory containing this SKILL.md>"
"$BHE_UI_SKILL_DIR/scripts/report-changed-lines.sh" \
  <absolute-worktree-path> origin/main
```

Report added lines using this exact order:

1. **Total PR additions**: all added production and committed test lines relative to the named base that are intended for the product PR.
2. **Production lines by feature**: attribute dedicated files and integration hunks to viewport controls, layout tools, relationship collapsing, export, or the current feature names. Call out shared integration separately when a hunk cannot be assigned cleanly.
3. **Committed test lines**: all added test lines included in the product PR.
4. **Deleted lines and PR net change**: report deletions separately when nonzero and calculate net change only from PR additions minus PR deletions.
5. **Standalone Playwright lines**: report additions in any local external harness separately. Explicitly exclude them from total PR additions, PR net change, and any line count appended to the Codex task title.

Use additions rather than whole-file size so existing code is not counted as feature code. Never include files outside the product PR in its totals, even when those files provide useful validation.

## Completion Gate

For PR-bound browser-visible work, capture at least one representative final-state screenshot from the validated task-owned environment. Add relevant theme, responsive, empty/error, or before-and-after states when they improve coverage. Keep local images outside the product diff, sanitize public artifacts, and report the paths and captions needed for stable PR-accessible uploads. Do not hand off a UI PR as ready while its required screenshot evidence is missing.

Hand off only after all of the following are true:

- the task-owned endpoint returns HTTP 200;
- the pre-change baseline and required post-change Playwright scenarios pass, unless an explicitly diagnostic or coverage-baselining ticket permits known failures;
- focused unit tests and static checks pass;
- no browser page errors remain;
- relevant WCAG AA checks are complete, with failures or unverified areas disclosed and resolutions suggested;
- the committed-test disposition, targeted/full-suite commands, results, artifacts, and CI-enforcement status are reported;
- the line-count summary is reported;
- the user receives the exact local URL and any necessary local login details.

When acceptance criteria explicitly permit failing diagnostic coverage, run the required scope, preserve the failure artifacts, enumerate the failures, and avoid claiming regression protection or accessibility conformance. Do not use this exception for ordinary implementation regressions.
