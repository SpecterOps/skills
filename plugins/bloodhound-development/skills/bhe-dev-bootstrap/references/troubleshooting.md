# BHE Local Troubleshooting

Read this reference when prerequisites, initialization, startup, login, or reset behavior fails.

## Diagnose First

```bash
git status --short --branch
just --list
docker info
docker compose --profile dev -f docker-compose.dev.yml ps
```

For isolated environments, run `bhe-isolated-stack.sh doctor`, `list`, `status`, and scoped `logs` before changing state.

## GitHub Access

```bash
ssh -T git@github.com
BHE_BASE_REPO=${BHE_BASE_REPO:-$HOME/Dev/bloodhound-enterprise}
git -C "$BHE_BASE_REPO" remote -v
git -C "$BHE_BASE_REPO" fetch --dry-run origin
```

If SpecterOps SAML SSO blocks access, authorize the SSH key for the SpecterOps organization in GitHub.

## Missing Yarn

The repository pins Yarn and includes its release file. Prefer Corepack. If `stbernard` cannot locate `yarn` or `yarnpkg`, create a narrow user-local shim only after confirming Node is available:

```bash
mkdir -p "$HOME/.local/bin"
printf '%s\n' \
  '#!/bin/sh' \
  'if [ -f .yarn/releases/yarn-4.13.0.cjs ]; then' \
  '  exec node .yarn/releases/yarn-4.13.0.cjs "$@"' \
  'fi' \
  'exec corepack yarn "$@"' > "$HOME/.local/bin/yarn"
chmod +x "$HOME/.local/bin/yarn"
ln -sf "$HOME/.local/bin/yarn" "$HOME/.local/bin/yarnpkg"

just modsync
just ensure-deps
```

## Installing Node Locally

Prefer the repository-supported Node version. If a user-local installation is necessary on Apple silicon, use the official ARM64 archive from `nodejs.org`, verify it against `SHASUMS256.txt`, and install under `~/.local`. Avoid system-wide installation unless requested.

Verify:

```bash
node --version
npm --version
corepack --version
```

## Docker Desktop

If `docker info` reports that the daemon is unavailable on macOS, open Docker Desktop, wait for the engine to become ready, and retry. Opening a GUI application may require user approval in the current execution environment.

## Local Login

For a new standard environment, run `scripts/configure-local-admin.sh` after `just init` and before first startup. The intended local credentials are `admin` / `admin`.

The configuration does not rewrite credentials already stored in a database volume. Verify an actual login before reporting credentials as working. Never delete a volume merely to enforce the default.

## Reset Behavior

Stop services without deleting data:

```bash
just bhe-dev down
```

Only reset when the user explicitly names the environment and requests it. Inspect current recipes first:

```bash
just --list | rg 'clear|volume|down|clean'
```

`just init clean` is a thorough reset path that rewrites default configuration, rebuilds without cache, and removes volumes. Treat it as destructive and require explicit approval.
