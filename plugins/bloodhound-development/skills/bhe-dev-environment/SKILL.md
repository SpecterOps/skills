---
name: bhe-dev-environment
description: Bootstrap, isolate, operate, and troubleshoot task-owned local BloodHound Enterprise (BHE) and BHCE development environments. Use for prerequisites, Git worktrees, `just init`, `just bhe-dev`, standard or isolated Docker/Compose stacks, local credentials, stack ownership, safe shutdown, and local startup failures. Route implementation, parity, enterprise review, and pull-request delivery to their focused BHE skills.
---

# BHE Dev Environment

Own the local worktree and runtime environment. Do not absorb product implementation, BHE/BHCE parity decisions, enterprise code review, or PR delivery; invoke `bhe-change-delivery` for those workflows and `bhe-enterprise-review` for review-only work.

## Operating Style

Match explanations to the user's experience. Explain risky, destructive, or externally consequential operations plainly before acting. Prefer repository-provided `just` recipes and bundled scripts over hand-running Docker, Go, or Yarn internals.

## Locations and Routing

Default locations:

- Base clone: `${BHE_BASE_REPO:-$HOME/Dev/bloodhound-enterprise}`
- Task worktrees: a sibling named `bloodhound-enterprise-<task-slug>` unless the user or repository uses another convention
- BHCE submodule: `<selected-worktree>/bhce`
- Standard local URL: `http://bhe.localhost/ui`

Verify rather than assume these paths.

Read only the references needed for the current task:

- Read [worktrees-and-isolation.md](references/worktrees-and-isolation.md) before selecting or creating a worktree, operating Docker, running parallel stacks, or changing stack state.
- Read [troubleshooting.md](references/troubleshooting.md) only when prerequisites, Yarn, Node, Docker, startup, login, or reset behavior fails.
- Invoke `bhe-sample-data-ingest` for sample data outside the isolated-stack helper.
- Invoke `bhe-ui-playwright` only after the task-owned environment is healthy.
- Invoke `bhe-change-delivery` for product edits, parity, validation, commits, PR preparation, rebases, CI follow-through, or PR-bound cleanup.

## Non-Negotiable Safety Rules

- Identify the owning worktree and Compose project before operating Docker. Never assume `bhe.localhost` belongs to the current task.
- Never stop, restart, remove, seed, or ingest into another task's stack.
- Never clear volumes, use `just init clean`, pass `-v` to shutdown, or delete stack state unless the user explicitly requests the exact reset.
- Use a fresh production-baseline worktree for new code-changing or PR-bound efforts unless the user explicitly names an existing worktree or branch.
- Treat each PR segment as a separate worktree, branch, stack identity, port slot, and URL.
- Run the isolated helper's `plan` before `up`; do not bypass its ownership checks with direct Compose commands.

## Delegated Environment Ownership

This skill is designed to run as the single environment-operator lane under `bhe-change-delivery` when environment work can overlap useful investigation or implementation. The orchestrator should delegate this whole lane rather than individual Docker commands. When used standalone or when no useful parallel work exists, operate the environment directly without spawning another agent.

Assign at most one environment operator for a task-owned stack. Resolve the worktree and stack identity before mutation, or limit the operator to read-only discovery when ownership is ambiguous. The same operator owns sample-data mutation through `bhe-sample-data-ingest`; do not assign ingest to a second concurrent agent. Require a handoff containing the worktree, branch, stack kind and identity, Compose project, slot and URL when applicable, health and login state, sample-data state, commands used, and exact safe restart and shutdown commands. No other agent may operate that stack concurrently.

Delegation never authorizes a destructive reset, another task's environment, a remote agreement, or a remote PR mutation.

## Select the Environment

For read-only diagnosis, inspect the named or current environment without creating a branch unless isolation is useful.

For new code-changing or PR-bound work:

1. Read [worktrees-and-isolation.md](references/worktrees-and-isolation.md).
2. Inspect existing worktrees and isolated-stack records.
3. Fetch `origin`.
4. Create a task branch and worktree from `origin/main` using `--no-track`.
5. Initialize submodules.
6. For BHCE feature work, follow **Start BHCE Work from BHCE Main** in the reference. Never use the submodule's pinned detached `HEAD` as the feature base.
7. Confirm the branch has no upstream before its first push.

Never build new PR work from whichever branch happens to be checked out in the base clone.

## Bootstrap a Standard Local Environment

Before operating a standard stack, check for the optional user-local Compose wrapper:

```bash
command -v bhe-local
```

When available, use `bhe-local <profile> ...` instead of `just bhe-dev` or direct Compose commands for standard stacks. The wrapper applies bounded logs and shared caches without changing a BHE repository. It preserves named volumes on `down`; never pass `-v` unless the user explicitly requests the exact reset.

Do not use `bhe-local` for fully isolated stacks. Continue to use the ownership-aware helper for every isolated-stack operation. PgAdmin and PgBadger are excluded by default; enable them only when the task needs them.

From the selected worktree:

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

3. Configure the local administrator before first startup:

   ```bash
   BHE_DEV_SKILL_DIR="<directory containing this SKILL.md>"
   "$BHE_DEV_SKILL_DIR/scripts/configure-local-admin.sh" \
     local-harnesses/build.config.json
   ```

4. Start and check the stack:

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

The intended local credentials are `admin@example.com` / `ChangeMe123!`. Existing database volumes may retain older credentials; verify login rather than inferring it from configuration.

## Use a Fully Isolated Stack

Use the bundled helper when a task needs independent backend services, database, credentials, data, or simultaneous end-to-end testing:

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

`--accept-standard-eula` authorizes acceptance only for `localhost`, `127.0.0.1`, or `*.localhost`. Never infer authorization for a remote host or another agreement. Omit the flag if the local database already accepted the EULA. Use `--skip-sample-data` only when the user explicitly wants an empty database.

Run `plan` before `up`. The helper enforces global ownership of names, worktrees, slots, projects, and hostnames. `down` preserves named volumes. See [worktrees-and-isolation.md](references/worktrees-and-isolation.md) for status, logs, seeding, and archival.

## Diagnose Before Changing State

When startup or tooling fails:

1. Capture the exact failing command, exit status, and useful error text.
2. Check the cheap explanations first: wrong worktree, wrong Compose project, unavailable daemon, missing prerequisite, stale recorded ownership, unhealthy dependency, or retained credentials.
3. Use `doctor`, `list`, `status`, and scoped `logs` for isolated stacks before changing state.
4. Distinguish a deterministic configuration failure from transient infrastructure failure; do not label a failure transient without evidence from more than one affected component or run.
5. Retry the same failed diagnostic or startup action no more than twice without a new hypothesis or changed condition.
6. Do not use reset or volume deletion as diagnosis. If the evidence points to retained state, explain the exact state and obtain explicit authorization before destructive recovery.

Read [troubleshooting.md](references/troubleshooting.md) for the relevant failure class. Report what was observed, what remains uncertain, and anything not verified.

## Release an Owned Stack Without Deleting Data

Release only an exactly identified task-owned stack, including when `bhe-change-delivery` routes here after terminal PR checks. Record the worktree, branch, stack identity, URL, preserved-data status, and restart command first.

For a standard stack:

```bash
if command -v bhe-local >/dev/null 2>&1; then
  bhe-local dev down
else
  just bhe-dev down
fi
```

For an isolated stack, use the recorded `name`, `slot`, and `repo` with `bhe-isolated-stack.sh down`. Verify only the task-owned containers stopped. Routine release preserves volumes, worktrees, branches, commits, and uncommitted files; it never archives state or performs a reset.
