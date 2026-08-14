# Plugins

Place installable plugin packages in this directory.

The canonical contributor workflow is documented in
[`CONTRIBUTING.md`](../CONTRIBUTING.md). This file describes the plugin-specific
layout and maintenance extension points.

Each cross-platform plugin should use:

```text
plugins/<plugin-name>/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── skills/
└── README.md
```

Optional plugin-owned content can include `commands/`, `hooks/`, `.mcp.json`, `assets/`, `scripts/`, and reference documentation.

After adding or changing a plugin, declare its ordering and publication surfaces
in `tools/maintenance/catalog.toml`, update its manifests and `ownership.json`,
then run `just generate-catalog`. Marketplace JSON and the marked root README
plugin table are generated; do not edit them by hand. `just check-catalog`
validates lifecycle, capabilities, ownership, manifest parity, and generated
drift without modifying files.

## Repository maintenance

The root `justfile` is the stable interface for repository maintenance:

- `just doctor` checks the local prerequisites. Python 3.13, `just`, and `uv`
  are required; optional platform tools are reported as visible skips.
- `just bootstrap-uv` creates a Git-ignored environment under
  `tools/maintenance/` containing the pinned `uv` version. It never installs
  globally.
- `just setup` bootstraps `uv` when needed, then creates the project-local
  environment from `uv.lock`. These two setup commands may use the network.
- `just fmt` formats only repository maintenance Python and its tests.
- `just fmt-check`, `just validate [target]`, `just test [target]`, and
  `just check` are offline and read-only. They never sync dependencies.
- `just check` is the aggregate local quality gate. Run `just setup` first.

Maintenance checks live in `tools/repo_maintenance/checks/`. A check module is
named `check_*.py` and exports one `CheckSpec` as `CHECK`; discovery is sorted
and requires no central registration edit. Check IDs must be unique and target
names must be stable. Only offline, non-mutating checks belong in that package.
Generators and network adapters use their packet-owned modules and explicit
`generate-*`, `refresh-*`, `check-external-*`, or `check-upstream-*` recipes.

Packet-specific recipes belong in the existing file under
`tools/maintenance/just/`.
The root `justfile` already imports those fragments so later packets do not
need to restructure the command surface.

GitHub Actions runs the same gate in `.github/workflows/quality.yml`. The check
names intended for branch protection are `Linux quality` and
`Windows PowerShell`. Enable them as required checks only after both jobs have
completed successfully on a pull request. The workflow is read-only; it does
not generate catalogs, refresh snapshots, check external links, or upload
activity reports.
