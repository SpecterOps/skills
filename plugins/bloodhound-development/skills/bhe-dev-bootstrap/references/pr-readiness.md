# BHE PR Readiness

Read this reference before committing, preparing, creating, updating, or monitoring a BHE pull request.

Before reaching **Prepare the Proposal**, complete [enterprise-code-review.md](enterprise-code-review.md). The proposed PR head must equal the enterprise review receipt's `head_sha`, and every applicable repository SHA must match the reviewed cross-repository candidate. Any product-code change after `PASS` invalidates that disposition. A focused closure review may certify narrow finding-driven fixes; a material redesign requires a fresh minimally briefed reviewer. A formatting-only or generated-only update may use a documented mechanical exception only when its source and representative output were already reviewed.

## Jira Context Gate

Before treating a behavioral change as ready for PR review, inspect the linked Jira ticket's applicable fields:

- **User Story:** Identify who or what benefits, the desired capability or behavior, and the intended outcome. Do not invent an artificial end user for technical work.
- **Description:** Explain the current problem or opportunity, why it matters, what prompted the change, and any relevant rationale, constraints, assumptions, or tradeoffs.
- **Acceptance Criteria:** State observable, testable outcomes, including important behavior that must remain unchanged and relevant boundaries, failure cases, compatibility requirements, or exclusions.
- **Testing Instructions:** Explain how to verify the acceptance criteria, including required setup or data, actions or commands, expected results, regression checks, automated tests, manual verification, and anything not tested with a reason.

Ensure the fields collectively explain the intended outcome, decision context, definition of success, and how success will be verified. Keep the depth proportional to the change's impact and ambiguity; omit inapplicable content rather than fabricating it.

When direct Jira access is unavailable, do not ask the user to grant access or sign in. Treat any field content the user has not pasted into the task as blank. Draft the applicable fields from the agreed scope, implementation evidence, validation results, and known constraints. Ask for existing wording only when it is necessary to avoid contradicting a known decision. This access limitation does not by itself block PR readiness.

Whenever drafting or revising Jira content, present it as standalone, field-by-field content the user can paste directly into Jira. Use the exact applicable field labels `JIRA — USER STORY`, `JIRA — DESCRIPTION`, `JIRA — ACCEPTANCE CRITERIA`, and `JIRA — TESTING INSTRUCTIONS`. Use task-list items for observable acceptance criteria. Do not mix commentary, citations, local file links, questions, confidence qualifiers, or approval language into the copy/paste blocks. Put unresolved questions or assumptions in a separate `Needs confirmation` section after the Jira-ready content. When only one field needs updating, output only that field. This output contract applies whether Jira content came from direct access, user-provided text, or a draft inferred from the implementation.

Draft missing or improved ticket content for the user's approval. Do not update Jira unless authorized. Distinguish incomplete documentation from unresolved alignment: draft missing wording from available evidence, but surface genuinely undecided outcomes, scope, or tradeoffs for appropriate product, design, or engineering input. Do not infer that synchronous refinement or approval by multiple roles is required unless established policy or the unresolved decision warrants it.

## Repository PR Template Gate

Read the pull-request template from the live target branch before drafting or creating a PR. Do not replace a repository template with a generic custom body.

```bash
git show <target-ref>:.github/pull_request_template.md
git ls-tree -r --name-only <target-ref> .github/PULL_REQUEST_TEMPLATE
```

Use `.github/pull_request_template.md` as the default. Use a specialized file under `.github/PULL_REQUEST_TEMPLATE/` only when the PR type calls for it. BHE and BHCE templates are independent and may differ; always use the template from the repository receiving the PR.

Preserve the selected template's section order, headings, issue-resolution syntax, change-type choices, and checklist. Replace instructional placeholders with concise project-specific content, select only applicable change types, and mark checklist items complete only when verified. Keep an inapplicable checkbox unchecked unless the template or repository convention says to remove it.

For browser-visible changes, capture focused screenshots from the task-owned validated environment when they materially help reviewers understand the result. Keep capture tooling and local images outside the product diff. Include screenshots in the template's screenshot section only after they have a stable PR-accessible URL; otherwise present the images and filled template to the user for approval before updating the PR.

Before creating or updating a PR, compare the proposed body with the selected template and confirm that no required section or checklist was omitted. If an existing PR body bypassed the template, prepare a template-compliant replacement and obtain the required approval before updating it.

## PR Trust Package Gate

Every proposed PR body must communicate the following trust package. Map the content into equivalent repository-template sections when they exist. Add a missing section when necessary, without duplicating information or disturbing required template syntax.

```text
INTENT
What behavior is changing and why?

IMPLEMENTATION
How was it implemented?
Include significant design decisions, tradeoffs,
or rejected alternatives when relevant.

BLAST RADIUS / RISK
What could break?
What systems or behaviors depend upon what changed?

VALIDATION / EVIDENCE
What evidence demonstrates that intended behavior works?
Include applicable automated tests/results, integration/E2E,
screenshots/recordings, browser validation, API responses,
logs/traces, performance results, migration validation.
Explicitly identify anything NOT validated.

TEST CHANGES
What tests were added, modified, removed, or intentionally omitted?
If expectations changed, why do the new expectations represent intended
behavior rather than accommodating a regression?

ROLLBACK
How can this change be reversed?
Include code reversion plus any feature flags, migrations, configuration,
persisted data, deployment ordering, or user-visible consequences.
```

Generate this content from the actual diff, repository context, and observed validation. Never claim evidence that was not observed. Use `Not applicable` or `Not validated` instead of silently skipping a relevant question. Keep the dedicated test-changes explanation even when the repository template has a general testing section. Tie validation evidence, screenshots, review-size calculations, and risk claims to the current PR head; refresh stale trust-package content after every material push or rebase.

Do not ask the authoring agent to assign R0–R3 or another risk tier. The authoring agent describes risk-relevant facts and blast radius; a separate independent review and classification process may challenge those claims and assign a tier later.

Jira remains the source for the problem, intended outcome, acceptance criteria, constraints, and planned verification. The PR remains the source for the actual implementation, observed blast radius, executed evidence, test changes, unvalidated areas, and rollback. Jira may contain overlapping context, but it does not replace any trust-package element in the PR. Reconcile material differences between the original plan and the implemented change explicitly.

## Reviewability Gate

Treat reviewability as separate from risk. A small authorization change can require expert review, while a large generated change can require little line-by-line inspection. Size never lowers a deterministic or independently assigned risk level.

Aim to keep each PR at or below **400 reviewable changed lines**. Calculate this from the merge base as additions plus deletions that require meaningful human inspection; do not use net line count or production additions alone.

Count hand-authored product code, tests, migrations, configuration and infrastructure code, schemas, fixtures, product catalogs, lookup tables, outbound destinations, and user-facing content whose correctness requires review. Tests count because assertions, expected values, skipped coverage, and altered behavior require substantive inspection.

Report separately, and exclude from the 400-line boundary only when their review burden is genuinely mechanical:

- generated code and generated clients;
- lockfiles, vendored dependencies, and build output;
- machine-updated snapshots or fixtures whose generation source and representative output were validated;
- binary assets;
- whole-file deletions after validating references and cleanup;
- trusted codemods, repository-wide renames, formatting-only changes, and other mechanical transformations that can be reviewed by inspecting the transformation and representative samples.

Do not exclude a category merely because it is large. If a reviewer must reason about individual lines for correctness, count them as reviewable. Do not collapse catalogs, configuration objects, fixtures, or assertions onto fewer physical lines to reduce the reported count; classify review burden according to the meaningful records and decisions a reviewer must inspect.

When the intended PR exceeds 400 reviewable changed lines:

1. Propose a decomposition into independently valid, testable, and deployable PRs. Consider preparatory refactors, backward-compatible contract steps, feature flags, stacked PRs, and separating mechanical work from behavioral work.
2. Test the decomposition against the trust package: each proposed segment must have standalone intent, implementation, blast radius, validation, test changes, and rollback rather than depending primarily on a later PR.
3. Prefer the decomposition when it preserves a coherent reviewer story and does not create incomplete behavior, dead scaffolding, duplicated validation, or a less safe intermediate state. Do not split solely to satisfy the numeric target.
4. If splitting is not feasible, explain concretely why independent pieces would be invalid, unsafe, misleading, or materially harder to verify. Convenience, implementation effort already spent, or a single Jira ticket is not sufficient justification.
5. Organize the unsplit diff so mechanical/generated changes and semantic changes are separable by file or commit when practical.
6. Provide a reviewer brief identifying critical files, invariants, generated/mechanical areas that need only sampling, and a suggested review sequence.
7. Surface the exception and obtain reviewer agreement before requesting full review.

Common legitimate exceptions include inseparable generated artifacts, atomic producer/consumer contracts with no safe compatibility state, tightly coupled schema and application invariants, large subsystem deletions, dependency upgrades with generated or lockfile changes, snapshot regeneration, trusted mechanical transformations, and security fixes that would create a vulnerable intermediate state. Treat these as examples requiring evidence, not automatic exemptions.

### Same-Repository Stacked PRs

When decomposition produces stacked PRs in the same repository, give every PR its own task branch and worktree, use the preceding PR branch as the next PR's temporary base, and add reciprocal dependency links. State the intended merge order and the behavior intentionally deferred to later segments. Require every segment to pass its own trust-package, enterprise-review, parity, validation, and rollback gates.

After a parent PR merges, fetch the live target branch, rebase or retarget the next PR as appropriate, recalculate its merge-base review size, refresh its trust package, and rerun affected validation before requesting review. Do not present a stacked child as independently ready while its required parent remains unresolved.

## BHE/BHCE Merge Runbook Gate

Treat the internal **Merge Requests — Or How To Merge With Confidence Across Dual Monorepos** runbook as an additional readiness gate. Its merge-request guidance applies to pull requests as well; translate legacy GitLab `MR`/`!####` notation into the link format used by the repository's current hosting platform.

For a change contained entirely in either BHCE or `bloodhound-enterprise`, fill out that repository's default PR template completely. Include the assigned ticket, the change's context and motivation, reproducible testing evidence, screenshots when they aid replication or review, and a truthfully completed checklist. No cross-repository coordination is required when there is no sister PR and no submodule change.

For enterprise development, make the BHCE submodule update intentional:

- Do not include a BHCE gitlink bump when the enterprise change does not require it.
- When the enterprise change depends on BHCE work, keep the BHCE and `bloodhound-enterprise` branches synchronized during review and point the enterprise branch at the exact BHCE review commit.
- After both changes merge, `bloodhound-enterprise/main` must point at the current BHCE `main` revision. Do not leave the enterprise main branch pinned to a feature-branch commit.

When work spans both repositories:

1. Create or update both PRs using each repository's own template.
2. Add a prominent reciprocal sister-PR link near the top of both descriptions so reviewers treat the changes as one review unit.
3. State the merge order and block both PRs until both are non-draft, have the required approvals, have no unresolved review threads other than the merge-order blocker, and have passing latest pipelines/checks.
4. Use a resolvable blocking thread when the hosting platform supports one. Otherwise add an explicit blocking comment or checklist item that cannot be mistaken for ordinary context.
5. Merge BHCE first. Then fetch BHCE `main`, update the enterprise gitlink to that merged revision, push the enterprise update after the required approval gate, wait for the resulting pipeline/checks, and merge BHE immediately when green.
6. If another merge introduces a conflict or invalidates the pipeline, resolve it and repeat the affected validation rather than merging with stale evidence.

Suggested blocking messages, adapted to current PR links:

```text
BHCE PR: Blocked until <BHE PR link> is approved and ready to merge. This PR merges first, but both PRs must be fully ready before either merge begins.

BHE PR: Blocked until <BHCE PR link> is approved and merged. After BHCE merges, update the submodule to the latest BHCE main revision, push that update, and merge this PR once the new checks pass.
```

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

Validate the enterprise review receipt immediately before presenting the proposal. Refuse to continue when the receipt is absent, is not `PASS`, reports an open blocking or important finding, does not match the current BHE/BHCE candidate SHAs, or omits required unverified areas and post-fix validation. At minimum, verify the current head locally:

```bash
test "$(git rev-parse HEAD)" = "<reviewed-head-sha>"
```

Fetch the live target and recompute the merge base. If target movement changes the effective PR diff, invalidate the stale receipt and repeat the affected review before requesting approval.

Present the proposed PR title and the complete proposed PR body as separate, self-contained copy/paste blocks. Do not interleave explanation, validation commentary, warnings, unresolved decisions, or the approval question inside either block. Put those items before or after the blocks. Preserve the repository template exactly within the proposed body.

Calculate the intended PR's line-count composition and Reviewability Gate result from the merge base with its current target branch, not from the previous commit or working-tree state alone. Use `git diff --numstat <merge-base>...HEAD`; classify additions and deletions as reviewable product code, tests, configuration/schema/migrations, documentation, or excluded generated/mechanical material. Reconcile category totals with Git's overall diff statistics, handle binaries and renames explicitly, and recalculate after any material commit or rebase. Show the reviewability assessment before requesting approval even when the PR is within the boundary.

When the PR exceeds 400 reviewable changed lines, uses an exception, or contains enough excluded material to make GitHub's headline count misleading, add a compact review-size statement to the proposed PR body rather than a large table. Use this form and omit empty categories:

```text
Review size: <reviewable total> reviewable changed lines — <product total> product, <test total> tests, and <config/schema/migration total> configuration/schema/migrations. Excluded mechanical/generated material: <excluded total> lines (<categories>). <If over 400: split plan or atomicity exception and reviewer agreement status.>
```

Keep CodeRabbit's summary and changed-files walkthrough as the detailed review aid; do not duplicate them. Omit the PR-body sentence when the change is within 400 reviewable lines and GitHub's aggregate count represents the review burden reasonably, unless the user requests a full LOC table. Still include the assessment in the approval proposal.

Use the Jira ticket as the source for the PR body's problem, intended behavior, rationale, and testing context when its content is available. When Jira content is unavailable, use the user-approved copy/paste draft as the provisional source. Do not silently create a competing account of the decision.

Do not automatically create or submit the PR.

## Required Approval Gate

Ask for explicit confirmation immediately before:

- creating or submitting a new PR;
- changing the title, body, checklist, labels, or other remote metadata of an existing PR;
- pushing additional commits to a branch with an existing open PR;
- rebasing or force-pushing a branch with an existing open PR;
- rerunning, canceling, or otherwise mutating remote CI checks.

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

After creating or updating a PR, monitor it unless the user asks to stop. Once GitHub confirms the expected head commit, create or update a current-task heartbeat automation that polls every ten minutes. Reuse a matching automation instead of creating a duplicate.

Configure the heartbeat to:

- target the exact PR URL and current head commit;
- record the exact task-owned stack identity and safe `down` command when Docker resources are running for that PR;
- report only material changes: a failed check, new actionable review feedback, a PR-state change, or all checks becoming terminal;
- inspect failed job logs enough to distinguish branch-related failures from unrelated baseline or infrastructure failures;
- avoid modifying code, pushing, rerunning jobs, dismissing feedback, or updating the PR without the applicable approval;
- continue through CodeRabbit completion and disposition of its actionable feedback for that head; if a finding requires a new push, monitor the approved replacement head instead;
- after terminal CI and feedback closure, execute **Release Task-Owned Docker Resources** unless the user requested a near-term keep-alive, and report the cleanup result before ending the heartbeat;
- stop polling only after reporting the terminal result and feedback disposition for the final monitored head;
- resume or replace monitoring after a later approved push changes the head commit.

Use the product's recurring automation mechanism when available. If it is unavailable, disclose that recurring monitoring could not be scheduled and use sparse, one-shot snapshots while the current turn remains active. Do not claim that monitoring will continue after the turn without an active automation.

Use sparse snapshots and report only changes:

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

### Release Task-Owned Docker Resources

Once all expected CI checks and CodeRabbit review are terminal for the current PR head, inspect every actionable finding and ensure it is either addressed in that head or answered with evidence. If a finding requires code changes, do not release the stack until the approved replacement head has completed the same follow-through. Human approval may remain pending; Docker is no longer required merely to keep the PR open.

Unless the user explicitly asks to keep the environment running for a near-term demo or investigation, reclaim the task-owned Docker resources after that terminal state:

1. Confirm the PR URL and head SHA, local branch and worktree, and that no pending validation requires the live environment.
2. Resolve the exact stack owner. For stacked or paired PRs, stop only the segment's exclusive stack; do not stop a shared stack or another segment's active environment.
3. Record the stack kind, isolated-stack `name` and `slot` when applicable, repository path, local URL, preserved-data status, and exact restart command in the final handoff.
4. Stop the owned standard stack with `bhe-local dev down` when available or `just bhe-dev down` from its owning worktree. Stop an isolated stack with the recorded ownership tuple:

   ```bash
   "<bhe-dev-bootstrap skill directory>/scripts/bhe-isolated-stack.sh" \
     down --name <task-slug> --slot <slot> --repo <worktree>
   ```

5. Verify that the task-owned containers stopped and report the reclaimed environment. Do not imply that another task's unrelated containers should also be stopped.

Routine release must preserve named volumes, worktrees, branches, local commits, and uncommitted files. Never pass `-v`, run `just init clean`, prune Docker globally, delete volumes, remove worktrees, or archive isolated-stack state during this cleanup. The PR and local Git history are sufficient to reconstruct the code, and the recorded start command can recreate the environment for a later demo. If ownership cannot be proven, do not guess; report the unresolved stack identity instead of stopping anything.
