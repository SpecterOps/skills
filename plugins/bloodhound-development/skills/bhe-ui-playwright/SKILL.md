---
name: bhe-ui-playwright
description: Validate BloodHound Enterprise (BHE) frontend changes with Playwright against task-owned local or isolated stacks. Use for BHE UI features, browser regressions, interaction testing, accessibility-oriented selectors, real API-backed end-to-end scenarios, WebGL/ReGraph controls, or repeated frontend iteration where a passing browser baseline and per-iteration line-count reporting are required.
---

# BHE UI Playwright

Validate BHE frontend work in a real browser without adding Playwright to the product repository unless the user explicitly requests it.

## Establish the Target

1. Use `bhe-dev-bootstrap` to identify the task-owned worktree, stack slug, URL, and credentials.
2. Verify the URL resolves only to `localhost`, `127.0.0.1`, or `*.localhost` before sending local credentials.
3. Verify the UI endpoint returns successfully.
4. Never reuse or restart another task's stack merely because it is available.

## Select the Harness

Prefer an existing Playwright setup in the product repository when one is already supported. Otherwise, use a standalone harness outside the BHE worktree so experimentation does not change product dependencies.

Default standalone harness location:

```text
$HOME/Documents/codex/experiments/bhe-playwright-pilot
```

Override it with `BHE_PLAYWRIGHT_HARNESS` when needed. If no harness exists, create one outside the product repository with `@playwright/test`, a Chromium project, retained failure traces/screenshots/video, and environment-driven `BHE_URL`, `BHE_USERNAME`, and `BHE_PASSWORD`. Request approval before downloading packages or browsers.

## Iteration Workflow

1. Run a passing Playwright baseline before changing product code.
2. Make the smallest feature change and its focused unit tests.
3. Extend the standalone scenario only for the behavior introduced in that iteration.
4. Run focused unit, type, lint, and formatting checks.
5. Run Playwright against the task-owned stack.
6. Verify the endpoint remains healthy and inspect browser errors.
7. Report cumulative line counts for the feature before handing control back to the user.

Do not commit, push, or prepare a PR unless the user separately requests it.

## Write Reliable Scenarios

- Prefer role, label, placeholder, and test-id locators over CSS or DOM structure.
- Assert the initial control state before interacting.
- Await the specific API response for workflows that depend on real data.
- Avoid fixed sleeps; wait for visible state, URL changes, responses, or enabled controls.
- Capture `pageerror` events and fail with their messages.
- Capture failed requests and unexpected HTTP 4xx/5xx responses caused by the exercised flow. Document intentional failures such as negative-test responses instead of silently ignoring them.
- Keep one worker for shared local environments unless tests are demonstrably isolated.
- Retain screenshots, video, and traces only on failure.
- Test graph data transformations and aggregation rules with unit tests. WebGL/canvas output is not fully observable through DOM assertions.

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

Hand off only after all of the following are true:

- the task-owned endpoint returns HTTP 200;
- the pre-change baseline and post-change Playwright scenario pass;
- focused unit tests and static checks pass;
- no browser page errors remain;
- relevant WCAG AA checks are complete, with failures or unverified areas disclosed and resolutions suggested;
- the line-count summary is reported;
- the user receives the exact local URL and any necessary local login details.
