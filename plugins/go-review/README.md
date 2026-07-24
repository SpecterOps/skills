# go-review

Security review plugin for Go HTTP/gRPC services and backend applications.

## Usage

Invoke with `/go-review:go-review`.

The skill prompts for:

- threat model: `REMOTE`, `LOCAL_UNPRIVILEGED`, or `BOTH`
- worker model: `haiku`, `sonnet`, or `opus`
- severity filter: `all`, `medium`, or `high`
- optional scope path

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

1. Build a conservative Go source inventory.
2. Select gated review clusters from `prompts/clusters/manifest.json`.
3. Spawn cluster workers.
4. Validate per-worker findings and coverage.
5. Run dedup and FP/severity judges.
6. Emit markdown and SARIF reports.
