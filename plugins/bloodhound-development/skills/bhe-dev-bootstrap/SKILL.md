---
name: bhe-dev-bootstrap
description: Bootstrap, run, isolate, troubleshoot, review, and validate local BloodHound Enterprise (BHE) development environments. Use when setting up BHE/BHCE locally, configuring prerequisites, running `just init` or `just bhe-dev`, diagnosing Docker/Compose failures, managing task-owned Git worktrees or isolated UI/full stacks, loading sample data, tracking BHE/BHCE parity, validating browser-visible work, reviewing BHE code for enterprise readiness and avoidable technical debt, or preparing and following through on BHE pull requests.
---

# BHE Dev Bootstrap

## Operating Style

Match explanations to the user's experience. Explain risky, destructive, or externally consequential operations plainly before acting. Prefer repository-provided `just` recipes and bundled skill scripts over hand-running Docker, Go, or Yarn internals.

For code-changing tasks, keep the Codex task title descriptive and append the current PR-review net changed-line count at meaningful handoffs, such as `Compact Explore Layout (+4)`. Calculate that count only from files intended for the product PR: additions minus deletions across the applicable BHE/BHCE repositories. Exclude standalone Playwright harnesses, local validation tooling, generated artifacts, and other files that will not be reviewed in the PR. Report excluded validation lines separately when useful. Omit line counts for read-only setup and diagnosis.

## Locations and Routing

Default locations:

- Base clone: `${BHE_BASE_REPO:-$HOME/Dev/bloodhound-enterprise}`
- Task worktrees: a sibling named `bloodhound-enterprise-<task-slug>` unless the user or repository uses another convention
- BHCE submodule: `<selected-worktree>/bhce`
- Local BHE URL: `http://bhe.localhost/ui`

Verify rather than assume these paths.

Read only the references needed for the current task:

- Read [worktrees-and-isolation.md](references/worktrees-and-isolation.md) before creating or selecting a worktree, operating Docker, running parallel UI/full stacks, or managing stack state.
- Read [troubleshooting.md](references/troubleshooting.md) when prerequisites, Yarn, Node, Docker, startup, login, or local reset behavior fails.
- Read [bhe-bhce-parity.md](references/bhe-bhce-parity.md) for every meaningful code change that could affect product behavior or compatibility.
- Read [enterprise-code-review.md](references/enterprise-code-review.md) after implementation stabilizes and before preparing the PR proposal.
- Read [pr-readiness.md](references/pr-readiness.md) before committing, preparing, creating, updating, or monitoring a PR.
- For browser-visible changes, invoke the separate `bhe-ui-playwright` skill after the task-owned environment is healthy.
- For sample data outside the isolated-stack helper, invoke the separate `bhe-sample-data-ingest` skill.

## Route Product-Domain Work

When the private SpecterOps `bloodhound` plugin is installed, keep environment ownership in this skill and route domain-specific work to its focused skills:

- Use `bloodhound-query` for Cypher search, saved-query, Explore, pathfinding, query-performance, or result-shape work.
- Pair query or graph behavior with `bloodhound-ad-analysis` or `azurehound-analysis` when AD/ADCS or Entra/Azure semantics are material.
- Use `bloodhound-opengraph` for custom node/edge schemas, OpenGraph extensions, ingestors, or hybrid graph modeling.
- Use `openhound-development` for OpenHound collector pipeline changes.
- Use `bloodhound-analysis` for live graph acceptance checks only when its MCP dependency is configured. Otherwise validate through the task-owned BHE/BHCE stack and API without claiming MCP-observed facts.

Treat these as domain and acceptance-test supplements. They do not replace task-owned worktree isolation, BHE/BHCE parity review, repository tests, accessibility validation, the enterprise review gate, or PR approval rules.

## Non-Negotiable Safety Rules

- Identify the owning worktree and Compose project before operating Docker. Never assume `bhe.localhost` belongs to the current task.
- Never stop, restart, remove, or ingest into another task's stack.
- Never clear volumes, use `just init clean`, or delete stack state unless the user explicitly requests the exact reset.
- Use a fresh production-baseline worktree for new code-changing or PR-bound efforts unless the user explicitly names an existing worktree or branch.
- Treat each PR segment as a separate worktree, branch, stack identity, port slot, and URL.
- Inspect BHCE implications for every meaningful BHE behavior or contract change.
- Do not create or update a remote PR without the approval required by [pr-readiness.md](references/pr-readiness.md).

## Select the Environment

For read-only diagnosis, inspect the named or current environment without creating a branch unless isolation is needed.

For new code-changing or PR-bound work:

1. Read [worktrees-and-isolation.md](references/worktrees-and-isolation.md).
2. Inspect existing worktrees and isolated stacks.
3. Fetch `origin`.
4. Create a task branch and worktree from `origin/main` using `--no-track`.
5. Initialize submodules.
6. For work that creates or modifies a BHCE branch, follow **Start BHCE Work from BHCE Main** in [worktrees-and-isolation.md](references/worktrees-and-isolation.md). Never use the submodule's pinned, detached `HEAD` as the BHCE feature base.
7. Confirm the branch has no upstream before its first push.

Never build new PR work from whichever branch happens to be checked out in the base clone.

## Bootstrap a Standard Local Environment

Before operating a standard stack, check for the optional local Compose wrapper:

```bash
command -v bhe-local
```

When available, use `bhe-local <profile> ...` instead of `just bhe-dev` or direct
Compose commands for standard stacks. The wrapper applies local log retention,
bounded Docker logs, a shared Go build cache, and opt-in database tools without
changing a BHE repository. It preserves named volumes on `down`; never pass `-v`
unless the user explicitly requests the exact reset. Existing containers receive
these settings only when recreated through `bhe-local up -d`.

Do not use `bhe-local` for fully isolated stacks. Continue to use the ownership-aware
isolated-stack helper for every isolated-stack operation. That helper applies the
same bounded Docker logs, PostgreSQL log retention, and shared Go build cache.
PgAdmin and PgBadger are excluded by default; pass `--with-db-tools` to `plan`
or `up` only when the task needs them.

From the selected BHE worktree:

1. Verify prerequisites:

   ```bash
   just --version
   go version
   node --version
   yarn --version
   docker --version
   docker compose version
   jq --version
   curl --version
   docker info
   ```

2. Initialize without deleting existing state:

   ```bash
   just init
   ```

3. Configure the development administrator before first startup:

   ```bash
   BHE_DEV_SKILL_DIR="<directory containing this SKILL.md>"
   "$BHE_DEV_SKILL_DIR/scripts/configure-local-admin.sh" \
     local-harnesses/build.config.json
   ```

4. Start and check the standard stack:

   ```bash
   if command -v bhe-local >/dev/null 2>&1; then
     bhe-local dev up -d
     bhe-local dev ps
   else
     just bhe-dev up -d
     docker compose --profile dev -f docker-compose.dev.yml ps
   fi
   curl -I http://bhe.localhost
   ```

5. For feature or browser testing, ensure representative graph data exists. Use `bhe-sample-data-ingest` for the standard stack and load both official AD and Entra datasets unless the user requests otherwise.

The configured local credentials are `admin` / `admin`. Existing database volumes may retain older credentials; verify login rather than inferring it from the configuration file.

## Use a Fully Isolated Stack

Use the bundled helper when a task needs independent backend services, database, credentials, dataset, or simultaneous end-to-end testing:

```bash
BHE_DEV_SKILL_DIR="<directory containing this SKILL.md>"

"$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh" doctor
"$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh" list
"$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh" next-slot
"$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh" plan \
  --name <task-slug> --slot <slot> --repo <absolute-worktree-path>
"$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh" up \
  --name <task-slug> --slot <slot> --repo <absolute-worktree-path> \
  --accept-standard-eula
```

`--accept-standard-eula` authorizes acceptance only for `localhost`, `127.0.0.1`, or `*.localhost`. Never infer authorization for a remote host or another agreement. Omit the flag if the local database has already accepted the EULA. Use `--skip-sample-data` only when the user explicitly wants an empty database.

Run `plan` before `up`. The helper enforces global ownership of stack names, worktrees, slots, projects, and hostnames. `down` preserves named volumes. See [worktrees-and-isolation.md](references/worktrees-and-isolation.md) for status, logs, seeding, and archival.

## Track BHE/BHCE Compatibility

For each meaningful change, read [bhe-bhce-parity.md](references/bhe-bhce-parity.md), inspect the corresponding BHCE surface, and record one disposition:

`matched`, `equivalent`, `bhe-only`, `intentionally-divergent`, `deferred`, or `investigate`.

Initialize one task-owned ledger after selecting the worktree:

```bash
PARITY_LOG="<directory containing this SKILL.md>/scripts/bhe-parity-log.sh"
"$PARITY_LOG" init --task <task-slug> --repo <absolute-worktree-path>
```

Use `check --stage iteration` during development and `check --stage pr` before PR handoff. An unresolved investigation, pending validation, missing required reference, or deferred item without a concrete follow-up blocks PR readiness.

Skip the ledger only for purely mechanical changes with no behavioral or compatibility implication.

## Validate Code Changes

- Establish a passing baseline before editing.
- Make narrow, recoverable changes and run the smallest relevant validation after each iteration.
- For browser-visible work, use `bhe-ui-playwright` and target WCAG 2.2 Level AA unless the repository specifies another AA version.
- Report known accessibility failures or unverified areas; do not claim conformance without evidence.
- Run relevant BHE tests for BHE-only code.
- Test both products for shared packages, APIs, schemas, generated clients, and shared contracts.
- Test BHCE plus the BHE consumer when changing `bhce/`.

## Run the Enterprise Code Review Gate

After the implementation and focused validation stabilize, read and follow [enterprise-code-review.md](references/enterprise-code-review.md). Review the complete intended PR diff plus enough surrounding code to evaluate design fit; do not treat passing tests or `just prepare-for-codereview` as a substitute.

Resolve correctness, security, compatibility, reliability, and material maintainability findings before PR preparation. Remove unjustified abstractions, duplication, dependencies, compatibility shims, and speculative flexibility. Prefer the smallest design that cleanly fits established repository patterns and leaves a clear path for future change.

Summarize the review evidence, findings, fixes, accepted tradeoffs, and remaining risks. Repeat the gate after any material review-driven change. Do not prepare the PR proposal or request PR approval while a blocking finding remains unresolved.

Continue following the before-commit requirements in [pr-readiness.md](references/pr-readiness.md) throughout development. After this gate passes, complete its proposal and approval requirements before any PR action.

## Stop Without Deleting Data

For the standard stack:

```bash
if command -v bhe-local >/dev/null 2>&1; then
  bhe-local dev down
else
  just bhe-dev down
fi
```

For an isolated stack, use its recorded `name`, `slot`, and `repo` with the helper's `down` command. Never use an unscoped `docker compose down` when multiple task environments may exist.
