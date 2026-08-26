---
name: go-review
description: Performs security review of arbitrary Go packages, including libraries, frameworks, CLIs, HTTP and gRPC services, and backend applications. Covers authentication and authorization, request parsing, SSRF, SQL and command injection, templates and filesystems, crypto/session handling, concurrency, and unsafe/cgo edges.
---

# Go Security Review

Runs in the main conversation. The orchestrator builds a Go inventory, selects
review clusters, delegates or sequentially executes their worker protocols,
validates artifacts, then runs dedup and FP/severity judges.

## When to Use

- Auditing Go HTTP, gRPC, GraphQL, or RPC services
- Reviewing backend APIs, daemons, gateways, proxies, or agents with network exposure
- Investigating authorization, SSRF, SQL, template, filesystem, concurrency, or cgo risk
- Reviewing Go libraries, frameworks, command-line tools, or packages without a service boundary

## When NOT to Use

- Smart contracts or blockchain modules with chain-specific semantics
- Kernel or eBPF code
- General Go style review without a security objective

## Rationalizations to Reject

- "Go is memory safe, so the code is safe." Most serious Go service bugs are trust-boundary and concurrency failures.
- "The middleware handles auth." Verify every route, interceptor, and alternate entry path.
- "The standard library prevents injection." It helps only when callers preserve its invariants.
- "This only affects internal services." Internal service credentials and metadata endpoints are still security boundaries.
- "The context will time out eventually." Missing cancellation and goroutine leaks become denial-of-service issues at scale.

## Required Inputs

Collect these once if they are not explicit. Do not ask for a worker model by
default; inherit the current session/client model. Honor a model only when the
user explicitly names one that the client makes available.

| Parameter | Values |
|-----------|--------|
| `threat_model` | `REMOTE`, `LOCAL_UNPRIVILEGED`, `BOTH` |
| `severity_filter` | `all`, `medium`, `high` |
| `scope_subpath` | optional; defaults to `.` |

## Orchestration Workflow

### Phase 1: Resolve Plugin Root

Resolve the directory containing `prompts/clusters/manifest.json` and
[go_inventory.go](../../scripts/go_inventory.go) from `${CODEX_PLUGIN_ROOT}`,
`${CLAUDE_PLUGIN_ROOT}`, or the installed location of this skill. Do not scan a
user's home directory. Abort with an actionable error if no root resolves.

Require Go 1.22 or newer. The inventory is implemented with the Go standard
library, uses the locally installed toolchain without automatic downloads, and
does not fetch the target's module dependencies. Source using syntax newer than
the installed Go version can still fail to parse.

### Phase 2: Build Go Inventory

Choose `output_dir` as `.go-review-results/<UTC timestamp>/`, or use an external
location requested by the user. Create it and run the inventory portably with:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/prepare_review.py" \
  --repo-root "." \
  --scope-subpath "${scope_subpath}" \
  --output-dir "${output_dir}"
```

Abort only if the inventory reports zero `.go` files. If `has_service=false`,
skip the service-boundary and request-input clusters and continue with any
other detected package capabilities.

The inventory schema remains at version 1. Its implementation uses Go syntax
trees for imports, declarations, calls, routes, goroutines, and channel types;
do not replace these results with text searches over source files.

This is conservative syntax analysis, not type or SSA analysis. It inventories
all matching non-test `.go` files regardless of build tags, crosses nested Go
modules within scope, and reports the review root's module in the top-level
`module` field. Capability heuristics can still over-select a cluster; workers
must verify reachability and data flow from source evidence.

### Phase 3: Write Context

Read `go-inventory.json` and write `context.md` with YAML frontmatter:

- `threat_model`
- `severity_filter`
- `scope_subpath`
- `go_file_count`
- `package_count`
- every capability flag from the inventory
- `output_dir`

The body must summarize:

- service entry points and frameworks
- untrusted input sources
- trust boundaries and auth assumptions
- outbound dependencies, storage, filesystem, templates, and crypto surfaces
- concurrency and cgo/unsafe surfaces

### Phase 4: Build Deterministic Run Plan

Run:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/build_run_plan.py" \
  --plugin-root "${GO_REVIEW_PLUGIN_ROOT}" \
  --output-dir "${output_dir}" \
  --threat-model "${threat_model}" \
  --severity-filter "${severity_filter}" \
  --scope-subpath "${scope_subpath}" \
  --context-roots "." \
  --has-service "${has_service}" \
  --has-outbound-http "${has_outbound_http}" \
  --has-sql "${has_sql}" \
  --has-exec "${has_exec}" \
  --has-fs-archive "${has_fs_archive}" \
  --has-template "${has_template}" \
  --has-crypto-auth "${has_crypto_auth}" \
  --has-concurrency "${has_concurrency}" \
  --has-unsafe-cgo "${has_unsafe_cgo}"
```

Read `plan.json`; do not manually re-derive cluster selection.

### Phase 5: Run Worker Protocols

The portable contracts are the bundled protocol files
`agents/go-review-worker.md`, `agents/go-review-dedup-judge.md`, and
`agents/go-review-fp-judge.md`. Do not assume those filenames are registered as
callable agent names. Read the relevant protocol and pass it with each rendered
prompt to the client-provided delegation mechanism. If delegation is not
available, execute each assignment sequentially in the main session while
preserving the same artifact contract.

Execution rules:

- optional foreground cache primer
- workers spawned foreground in waves of at most 16
- no `run_in_background=true`
- pass each rendered worker prompt verbatim
- each worker writes findings, shard, and coverage artifacts
- inherit the current session/client model unless the user explicitly selected an available model

If `plan.json` contains zero workers, create an empty `findings-index.txt`, note
that no capability-gated clusters were selected in `run-summary.md`, and proceed
to reporting. Do not treat an ordinary package with no selected clusters as a
workflow failure.

### Phase 6: Validate Worker Artifacts

For each completed worker, run:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/validate_artifacts.py" \
  "${output_dir}/plan.json" \
  --worker "worker-N" \
  --claimed-count "worker-N=<count>"
```

After all workers complete, reconcile shards and initialize deterministic empty
reports when applicable:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/finalize_run.py" "${output_dir}"
```

This builds `findings-index.txt` from the union of worker shards and
`findings/*.md`, retains orphan findings, and records incomplete shards in
`run-summary.md`; do not silently drop a finding because a worker crashed after
writing it.

### Phase 7: Judges and Reports

Run the bundled dedup protocol, then the bundled FP protocol, each with
`output_dir` in the prompt. The FP judge also receives the absolute path to
[generate_sarif.py](../../scripts/generate_sarif.py). Use delegated workers when
available or execute these protocols sequentially in the main session.

Always run the SARIF safety net:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/generate_sarif.py" "${output_dir}"
```

Return `REPORT.md`, `REPORT.sarif`, `go-inventory.json`, and `run-summary.md`.

## Success Criteria

- `go-inventory.json` exists and reports at least one Go file
- every planned worker has a coverage file and shard
- `findings-index.txt` exists even for zero findings
- `dedup-summary.md`, `fp-summary.md`, `REPORT.md`, and `REPORT.sarif` exist
- any truncated or failed worker is surfaced in `run-summary.md`

## Artifact Sensitivity

`.go-review-results/` may contain source excerpts, suspected vulnerabilities,
and absolute local paths. Treat it as sensitive assessment data. Before sharing
or committing it, review and redact the contents. Recommend that users ignore
the directory in the target repository or choose an external output location,
but do not modify `.gitignore` without permission.

## Source Provenance

The implementation approach and security-review taxonomy are annotated in
[references/provenance.md](../../references/provenance.md). Treat those sources
as guidance; findings still require evidence from the repository under review.
