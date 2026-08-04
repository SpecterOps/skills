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

## Rebase an Existing PR Safely

Before rebasing, distinguish the PR's recorded base commit from the live branch tip. Do not treat `baseRefOid` from `gh pr view` as proof of current `origin/main`; resolve or fetch the live ref directly.

When BHE/BHCE ancestry is relevant, inspect all three live values before claiming that a PR is unaffected:

- the current BHE `main` commit;
- the BHCE gitlink recorded by that BHE commit;
- the current BHCE `main` commit and whether the gitlink is its ancestor.

```bash
git fetch origin main
git -C bhce fetch origin main
bhe_main=$(git rev-parse origin/main)
bhce_pin=$(git ls-tree "$bhe_main" bhce | awk '{print $3}')
git -C bhce fetch origin "$bhce_pin"
git -C bhce merge-base --is-ancestor "$bhce_pin" origin/main
```

An ancestry check exit code of `0` is valid; `1` means the histories diverged or the pin is not an ancestor. Resolve the live BHE ref directly instead of substituting a PR's recorded base SHA.

For BHCE feature work, use BHCE `origin/main` as the feature base regardless of the detached commit initially checked out by BHE. Verify the BHCE remote and branch setup using **Start BHCE Work from BHCE Main** in [worktrees-and-isolation.md](worktrees-and-isolation.md).

If the inherited BHE pin is not an ancestor but its tree matches BHCE `origin/main`, record the exact SHAs and classify it as a tree-equivalent baseline condition. Do not rebase the BHCE feature onto the detached pin, rebuild a correctly based feature branch, or treat the expected local `M bhce` checkout as a merge conflict. Investigate a differing tree as a compatibility risk.

A BHE-only PR that does not modify `bhce` may remain GitHub-mergeable while current BHE `main` carries an invalid BHCE pin. Rebasing that PR inherits the live pin; GitHub mergeability does not enforce the repository's submodule-ancestry policy. Existing CI may also predate the problematic pin.

When both repositories need rebasing, always rebase BHCE first and BHE second:

1. Fetch BHCE `origin/main` and rebase the BHCE task branch onto it.
2. Validate the rebased BHCE change and, after the required approval, update its remote PR branch.
3. Fetch BHE `origin/main` and rebase the BHE task branch.
4. Update and stage the BHE `bhce` gitlink only after the BHCE target commit is settled.

Once the required BHCE change is present on BHCE `main`, normally point BHE at the latest fetched BHCE `origin/main` commit. This preserves ancestry and avoids manufacturing a tree-equivalent commit on a disconnected history. While a paired BHCE PR is still unmerged, BHE may temporarily pin the exact rebased BHCE PR head; document that dependency and update the gitlink to BHCE `main` after the BHCE PR merges.

After explicit rebase approval, use this sequence from a clean task worktree:

```bash
git status --short --branch
git fetch origin main
git rebase origin/main
git submodule update --init --recursive bhce
git status --short --branch
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
git ls-tree HEAD bhce
```

The submodule checkout may appear modified immediately after a successful BHE rebase because the working checkout still points at the old commit. Synchronize it with `git submodule update`; do not stage that checkout mismatch as a new gitlink change.

Reassess the parity ledger and validation evidence after the rebase. If the inherited BHE pin is not an ancestor of BHCE `main`, report that baseline issue explicitly; do not imply that an unrelated BHE diff repairs it.

Updating the open PR requires separate explicit approval. Immediately before the approved push, refresh the remote branch, then protect remote-only work with a lease:

```bash
git fetch origin <pr-branch>
git push --force-with-lease origin <pr-branch>
gh pr view <pr-number> --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup,reviewDecision
```

Confirm that GitHub attached the rewritten head and started the expected checks. Do not use plain `--force`.

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
