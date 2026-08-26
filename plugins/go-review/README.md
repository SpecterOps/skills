# go-review

Security review plugin for Go packages, libraries, frameworks, CLIs, HTTP/gRPC
services, and backend applications.

Status: active. Supported clients: Codex and Claude.

## Prerequisites

- Go 1.22 or newer for the AST-backed source inventory
- Python 3.11 or newer for run planning, artifact validation, and SARIF generation

The inventory uses only the Go standard library and runs with the locally
installed Go toolchain; it does not download analyzer dependencies or Go
toolchains. Reviewing a target with private modules does not require the
inventory step to resolve or fetch those modules. Source using syntax newer
than the installed Go version can still fail to parse.

## Usage

Invoke with `/go-review:go-review`.

The skill prompts for:

- threat model: `REMOTE`, `LOCAL_UNPRIVILEGED`, or `BOTH`
- severity filter: `all`, `medium`, or `high`
- optional scope path

Workers inherit the current ChatGPT/Codex or client model. A different model is
used only when the user explicitly selects one available in that client.

## What It Reviews

- authentication and authorization boundaries
- request parsing and body limits
- outbound HTTP and SSRF
- SQL and storage access
- command execution
- template rendering and XSS
- filesystem and archive extraction
- JWT, TLS, cookie, and session handling
- goroutine, timeout, cancellation, and shared-state hazards
- `unsafe` and cgo boundaries

## Outputs

Findings are written to `.go-review-results/<timestamp>/`:

- `go-inventory.json`
- `context.md`
- `plan.json`
- `findings/`
- `coverage/`
- `REPORT.md`
- `REPORT.sarif`

## Architecture

The plugin follows the same review pipeline as `c-review` and `rust-review`:

1. Build a conservative Go source inventory with Go's parser and AST packages.
2. Select gated review clusters from `prompts/clusters/manifest.json`.
3. Spawn cluster workers.
4. Validate per-worker findings and coverage.
5. Run dedup and FP/severity judges.
6. Emit markdown and SARIF reports.

The AST-backed inventory understands Go import declarations, aliases, function
and method declarations, calls, goroutines, and channel types. This avoids
treating comments and string literals as code while keeping the version 1
inventory schema used by the rest of the plugin.

It is conservative syntax analysis rather than type-aware or SSA analysis.
Build-tagged files and nested modules are included within the selected scope;
the top-level `module` field identifies the review root. Import and call
heuristics may activate an irrelevant cluster, so report findings only after
verifying concrete reachability and data flow.

The version 1 inventory schema remains compatible with the reporting pipeline.
The analyzer entry point changed in 0.2.0 from `go_inventory.py` to
`go_inventory.go` and therefore requires Go 1.22 or newer.

## Sensitive Outputs

`.go-review-results/` can contain source excerpts, unconfirmed vulnerability
candidates, and absolute local paths. Do not commit or publish it without
reviewing and redacting the contents. Prefer adding it to the target project's
ignore rules or writing results outside the repository.

See [source provenance](references/provenance.md) for the primary sources that
informed the design and review taxonomy.

## Support and Release

- Support: [SpecterOps Skills issues](https://github.com/SpecterOps/skills/issues)
- Current release: 0.3.0
