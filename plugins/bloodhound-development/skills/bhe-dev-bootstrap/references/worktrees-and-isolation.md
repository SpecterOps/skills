# BHE Worktrees and Isolation

Read this reference before selecting or creating worktrees, operating Docker, or running parallel BHE environments.

## Create a Task Worktree

Use a fresh worktree for new code-changing or PR-bound work. Read-only diagnosis does not require one unless isolation is useful.

```bash
BASE_REPO=${BHE_BASE_REPO:-$HOME/Dev/bloodhound-enterprise}
TASK_SLUG=<task-slug>
WORKTREE="$(dirname "$BASE_REPO")/bloodhound-enterprise-$TASK_SLUG"
BRANCH=<short-feature-branch>

git -C "$BASE_REPO" worktree list --porcelain
git -C "$BASE_REPO" branch --list "$BRANCH"
git -C "$BASE_REPO" fetch origin
git -C "$BASE_REPO" worktree add --no-track -b "$BRANCH" "$WORKTREE" origin/main
git -C "$WORKTREE" submodule update --init --recursive
git -C "$WORKTREE" status --short --branch
```

Confirm the branch has no upstream before its first push:

```bash
if git -C "$WORKTREE" rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
  printf 'Unexpected upstream: '
  git -C "$WORKTREE" rev-parse --abbrev-ref '@{upstream}'
  exit 1
fi
```

If the path or branch exists, inspect it. Reuse it only when it belongs to the same task and has the intended baseline. Treat each PR segment as a distinct identity even when several segments share an umbrella feature.

## Start BHCE Work from BHCE Main

Apply this only when the task will create or modify a BHCE branch. Initialize BHE from BHE `origin/main`, but create the BHCE feature branch explicitly from BHCE `origin/main`; never branch from the submodule's pinned, detached `HEAD`.

```bash
BHCE_BRANCH=<bhce-feature-branch>

git -C "$WORKTREE/bhce" remote get-url origin
git -C "$WORKTREE/bhce" fetch origin main
git -C "$WORKTREE/bhce" switch --no-track -c "$BHCE_BRANCH" origin/main
git -C "$WORKTREE/bhce" status --short --branch
```

Require the BHCE origin to be:

```text
git@github.com:SpecterOps/BloodHound.git
```

If it points to a local clone or another remote, stop and inspect the task-owned checkout before changing it. Do not silently inherit that remote as the feature source.

Leave the pinned, detached BHCE checkout alone for BHE-only work. Do not mass-repair dirty or older workspaces; preserve their in-progress state and never use them as another feature's baseline.

## Identify Stack Ownership

Before operating Docker:

```bash
docker ps --format '{{.Names}}' | sort
docker inspect <container> --format '{{json .Config.Labels}}'
```

Never assume `bhe.localhost` belongs to the current worktree. Avoid unscoped Compose operations.

For the standard stack, run Compose commands from its owning worktree:

```bash
docker compose --profile dev -f docker-compose.dev.yml ps
docker compose --profile dev -f docker-compose.dev.yml logs -f bhe-api
docker compose --profile dev -f docker-compose.dev.yml logs -f bhe-ui
```

## Choose Isolation

Use isolated UI when frontend tasks can share one healthy backend and dataset:

```bash
TARGET_PROXY_URL=http://bhe.localhost \
  yarn workspace bloodhound-enterprise-ui dev --host 127.0.0.1 --port <unique-port>
```

Open `http://127.0.0.1:<unique-port>/ui`. Record and stop only the process that owns this UI.

Use a fully isolated stack when tasks need independent source, backend, database, credentials, data, or simultaneous end-to-end testing. Do not run the repository Compose file directly for parallel full stacks because it contains fixed defaults.

## Isolated-Stack Helper

```bash
BHE_DEV_SKILL_DIR="<directory containing this skill's SKILL.md>"
STACK="$BHE_DEV_SKILL_DIR/scripts/bhe-isolated-stack.sh"
```

Inspect prerequisites and ownership:

```bash
"$STACK" doctor
"$STACK" list
"$STACK" list --json
"$STACK" next-slot
```

Create and start:

```bash
"$STACK" plan --name <task-slug> --slot <slot> --repo <worktree>
"$STACK" up --name <task-slug> --slot <slot> --repo <worktree> \
  --accept-standard-eula
```

PgAdmin and PgBadger are excluded by default. Add `--with-db-tools` to `plan`
or `up` when they are needed, or `--without-db-tools` to explicitly return a
recorded stack to the default on its next `up`. Both choices preserve named
volumes.

The helper:

- removes fixed API container naming with a generated override;
- uses file-based Traefik routing with Docker discovery disabled;
- allocates deterministic ports from the slot;
- creates task-specific hostnames, networks, volumes, and configuration;
- rejects stack name, project, worktree, slot, or hostname ownership collisions;
- serializes reservation and archival state changes across concurrent helper processes;
- records state under `${XDG_STATE_HOME:-$HOME/.local/state}/codex-bhe-stacks`;
- bounds Docker JSON logs and retains only the newest PostgreSQL log files;
- shares a named Go build cache across isolated API containers;
- keeps PgAdmin and PgBadger opt-in rather than running them for every task;
- seeds missing official AD and Entra data unless `--skip-sample-data` is explicitly used.

EULA acceptance requires `--accept-standard-eula` and is refused for non-local hostnames. Once the database records acceptance, later `up` or `seed` calls do not need the flag.

Inspect and troubleshoot only the owned stack:

```bash
"$STACK" status --name <task-slug> --slot <slot> --repo <worktree>
"$STACK" logs --name <task-slug> --slot <slot> --repo <worktree>
"$STACK" logs --name <task-slug> --slot <slot> --repo <worktree> --service bhe-api
```

Seed an already-running stack:

```bash
"$STACK" seed --name <task-slug> --slot <slot> --repo <worktree> \
  --accept-standard-eula
```

Stop without deleting named volumes:

```bash
"$STACK" down --name <task-slug> --slot <slot> --repo <worktree>
```

Archive state only after the stack is stopped:

```bash
"$STACK" archive --name <task-slug> --slot <slot> --repo <worktree>
```

Archival moves the manifest and generated configuration under the helper's `archive` directory. It does not delete Docker volumes. Archived manifests remain ownership records: their stack name, Compose project, worktree, slot, and hostname cannot be reused while the preserved named volumes may still exist. Never archive state as a substitute for resetting or deleting data.

The helper intentionally has no destructive retirement command. Retire archived ownership only through a separate, explicit cleanup: first verify and remove the archived stack's named volumes using its recorded Compose project identity, then delete that one archived state directory. Do not delete an archived ownership record while its volumes remain.

## Sample-Data Expectations

For new feature environments, load both official Active Directory and Entra datasets unless the user requests a narrower dataset. Verify new ingest jobs report no failed or partially failed files and that available environments include `active-directory` and `azure`.

Existing environments are used only as a coarse skip signal. Their presence does not prove historical ingest completeness; investigate suspicious or incomplete graph behavior with the `bhe-sample-data-ingest` skill.
