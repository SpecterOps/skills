# BHE PR Readiness

Read this reference before committing, preparing, creating, updating, or monitoring a BHE pull request.

Before reaching **Prepare the Proposal**, complete [enterprise-code-review.md](enterprise-code-review.md). If implementation changes materially afterward, repeat that review before requesting PR approval.

## Jira Context Gate

Before treating a behavioral change as ready for PR review, inspect the linked Jira ticket's applicable fields:

- **User Story:** Identify who or what benefits, the desired capability or behavior, and the intended outcome. Do not invent an artificial end user for technical work.
- **Description:** Explain the current problem or opportunity, why it matters, what prompted the change, and any relevant rationale, constraints, assumptions, or tradeoffs.
- **Acceptance Criteria:** State observable, testable outcomes, including important behavior that must remain unchanged and relevant boundaries, failure cases, compatibility requirements, or exclusions.
- **Testing Instructions:** Explain how to verify the acceptance criteria, including required setup or data, actions or commands, expected results, regression checks, automated tests, manual verification, and anything not tested with a reason.

Ensure the fields collectively explain the intended outcome, decision context, definition of success, and how success will be verified. Keep the depth proportional to the change's impact and ambiguity; omit inapplicable content rather than fabricating it.

When direct Jira access is unavailable, do not ask the user to grant access or sign in. Treat any field content the user has not pasted into the task as blank. Draft the applicable fields from the agreed scope, implementation evidence, validation results, and known constraints, then provide clearly labeled, copy/paste-ready Jira content for the user. Ask for existing wording only when it is necessary to avoid contradicting a known decision. This access limitation does not by itself block PR readiness.

Draft missing or improved ticket content for the user's approval. Do not update Jira unless authorized. Distinguish incomplete documentation from unresolved alignment: draft missing wording from available evidence, but surface genuinely undecided outcomes, scope, or tradeoffs for appropriate product, design, or engineering input. Do not infer that synchronous refinement or approval by multiple roles is required unless established policy or the unresolved decision warrants it.

## Before Committing

Inspect repository instructions and the complete diff:

```bash
git status --short --branch
git diff
git diff --staged
git diff --check
```

Review both staged and unstaged changes. Confirm that staged files contain only the intended work, remove temporary diagnostics, and check that credentials, tokens, private keys, customer data, and local-only configuration are absent. When a case-only rename is intended on a case-insensitive filesystem, verify that Git recorded it as a rename; use an intermediate `git mv` name when necessary.

When `gitleaks` or `trufflehog` is already available, run a local, redacted secret scan before PR handoff for changes involving authentication, configuration, fixtures, logs, or generated artifacts. Keep scanner output outside the product diff and never reproduce raw secret values in the handoff. If no scanner is available, record the manual staged-diff check rather than downloading tooling without approval.

`AGENTS.md` requires:

```bash
just prepare-for-codereview
```

Run it before every commit unless current repository instructions explicitly change. Because it is comprehensive, prefer a small number of meaningful commits over frequent unprepared checkpoints. Use the working tree and targeted tests for intermediate recovery.

Commit only intended files using the repository's signed-commit setup:

```bash
git add <files>
git commit -m "<type>: <short description>"
```

For work spanning tasks, leave a recoverable handoff with `git log --oneline -5`, status, validation results, and the latest diff.

## Parity Gate

For meaningful changes:

```bash
PARITY_LOG="<bhe-dev-bootstrap skill directory>/scripts/bhe-parity-log.sh"

"$PARITY_LOG" check --task <task-slug> --stage pr
"$PARITY_LOG" show --task <task-slug>
```

The final ledger must include:

- a resolved BHE/BHCE disposition;
- completed BHE and BHCE validation, or a concrete explanation that BHCE testing is not required;
- a non-pending BHE commit or PR reference;
- a non-pending BHCE reference for `matched` or `equivalent`;
- a concrete follow-up for `deferred`;
- intentional differences and remaining risks.

## Prepare the Proposal

Use the current `AGENTS.md` PR title format:

```text
<conventional commit tag>: <Title> <Jira tag>
```

Before requesting approval, show:

- linked Jira ticket and a concise context-readiness recap;
- enterprise code-review scope, findings, fixes, accepted tradeoffs, and remaining risks;
- proposed title and body;
- base and head branches;
- commit summary;
- completed checks and accessibility recap when applicable;
- parity disposition and validation evidence;
- known failures, risks, or unverified areas.

Use the Jira ticket as the source for the PR body's problem, intended behavior, rationale, and testing context when its content is available. When Jira content is unavailable, use the user-approved copy/paste draft as the provisional source. Do not silently create a competing account of the decision.

Do not automatically create or submit the PR.

## Required Approval Gate

Ask for explicit confirmation immediately before:

- creating or submitting a new PR;
- pushing additional commits to a branch with an existing open PR;
- rebasing or force-pushing a branch with an existing open PR.

A request to prepare a PR does not authorize submission. A direct request to create the PR authorizes that immediate creation only. If implementation changes afterward, ask again before pushing to the open PR.

For BHCE changes, commit and push inside `bhce/` first, then update the BHE submodule pointer when appropriate.

## Follow Through

After creating a PR, monitor it unless the user asks to stop. Use sparse, one-shot snapshots and report only changes:

```bash
gh pr view <pr-number> --json statusCheckRollup,comments,reviews
```

Do not use `gh pr checks --watch` unless the user explicitly requests active monitoring.

Treat automated review comments as hypotheses:

1. Summarize actionable items.
2. Inspect the code before agreeing.
3. Explain why no change is needed, or prepare a local fix.
4. Obtain explicit approval before pushing the fix to the open PR.

For CI failures, inspect the failed job rather than all logs:

```bash
gh run view <run-id> --job <job-id> --log-failed
```

Identify whether the failure is related to the PR and fix or report it before declaring readiness.
