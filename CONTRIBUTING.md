# Contributing

Thank you for improving SpecterOps Skills. Contributions to documentation,
plugin metadata, compatibility, tests, maintenance automation, and packaged
capabilities are welcome.

## Before you start

1. Open an issue for changes that add a plugin, alter a public interface, change
   publication surfaces, or require a licensing decision.
2. Never commit credentials, customer data, operational evidence, or local
   machine paths.

## Development environment

The maintenance framework requires Python 3.13, Go 1.22 or newer, just, and uv. Exact maintained
versions are recorded in `tools/maintenance/toolchain.toml`.

The easiest setup is the checked-in Dev Container configuration. Open the
repository in a Dev Container-compatible editor and allow its post-create
command to install the pinned just and uv versions and synchronize the locked
maintenance environment.

For a local setup:

```bash
just bootstrap-uv
just setup
just doctor
```

`just bootstrap-uv` and `just setup` use the network and only create ignored
repository-local environments. The validation commands below are offline and
read-only.

## Make and validate a change

Run the complete local gate before opening a pull request:

```bash
just check
```

Useful narrower commands are:

```bash
just fmt-check
just validate
just test
just go-review-test
just check-catalog
just check-inventory
just check-powershell
```

Use `just fmt` to format maintenance Python. Generators are intentionally
separate from the read-only gate:

```bash
just generate-catalog
just generate-inventory
```

Commit generated outputs with the source metadata that produced them.

## Scaffold plugin metadata

Plan a new metadata-only plugin before creating files:

```bash
just scaffold-plugin-metadata example-plugin \
  "Example workflows for a focused use case."
```

The default plan includes Codex and Claude manifest templates, an incubating
ownership record, release/support metadata, an icon, and a complete plugin
README. It does not create skills or publish an empty plugin to Claude.

Review the plan, then apply it explicitly:

```bash
just scaffold-plugin-metadata example-plugin \
  "Example workflows for a focused use case." mode=apply
```

Use `manifests=codex` when a Claude manifest is not wanted. Maintainers and
support can be supplied with `maintainer=...` and `support_url=...` named
arguments. After capabilities are added, update `ownership.json`, publication
surfaces in `tools/maintenance/catalog.toml`, and manifest prompts together.

## Plugin contribution checklist

- The plugin name uses lowercase hyphen-separated words.
- `ownership.json` matches the packaged skills and agents.
- Manifests agree on name, version, and description.
- The plugin README states status, prerequisites, supported clients, example
  prompts, support, and release information.
- External tools, MCP servers, credentials, network access, and platform
  requirements are documented.
- Generated marketplaces and root inventory are current.
- `just check` passes without modifying the worktree.

## Pull requests

Use a conventional commit subject when practical, explain user-visible impact,
and include the commands used for verification. Complete the pull request
template and call out any platform-specific checks that could not be run.

## Getting help

Use a GitHub issue for reproducible defects or focused proposals. Do not include
secrets, sensitive assessment data, or vulnerability details in a public issue;
coordinate privately with the maintainers when disclosure could create risk.
