---
name: go-review
description: Performs comprehensive Go service security review for authentication and authorization flaws, request parsing issues, SSRF, SQL and command injection, template and filesystem bugs, crypto/session mistakes, concurrency hazards, and unsafe/cgo edges. Use when auditing Go HTTP or gRPC services, backend APIs, daemons, or network-facing Go applications.
allowed-tools: Agent AskUserQuestion SendMessage TaskCreate TaskUpdate TaskList Read Write Bash
---

# Go Service Security Review

Runs in the main conversation. The orchestrator builds a Go inventory, selects
review clusters, spawns workers, validates artifacts, then runs dedup and
FP/severity judges.

## When to Use

- Auditing Go HTTP, gRPC, GraphQL, or RPC services
- Reviewing backend APIs, daemons, gateways, proxies, or agents with network exposure
- Investigating authorization, SSRF, SQL, template, filesystem, concurrency, or cgo risk

## When NOT to Use

- Pure libraries with no service surface
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

Collect these once with `AskUserQuestion` if they are not explicit:

| Parameter | Values |
|-----------|--------|
| `threat_model` | `REMOTE`, `LOCAL_UNPRIVILEGED`, `BOTH` |
| `worker_model` | `haiku`, `sonnet`, `opus` |
| `severity_filter` | `all`, `medium`, `high` |
| `scope_subpath` | optional; defaults to `.` |

## Orchestration Workflow

### Phase 1: Resolve Plugin Root

Resolve the directory containing `prompts/clusters/manifest.json` and
[go_inventory.py](../../scripts/go_inventory.py) using `${CLAUDE_PLUGIN_ROOT}`, `${CODEX_PLUGIN_ROOT}`, then:

```sh
find ~/.claude ~/.codex . -path '*/plugins/go-review/prompts/clusters/manifest.json' -print -quit 2>/dev/null
```

Abort if no root resolves.

### Phase 2: Build Go Inventory

Create `output_dir` at `.go-review-results/<utc timestamp>/` and pre-create the
worker artifact directories:

```sh
mkdir -p "${output_dir}/findings" "${output_dir}/findings-index.d" "${output_dir}/coverage"
```

Then run:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/go_inventory.py" \
  --repo-root "." \
  --scope-subpath "${scope_subpath}" \
  --output "${output_dir}/go-inventory.json"
```

Abort if the inventory reports zero `.go` files or `has_service=false`. This v1
plugin intentionally targets service code, not generic libraries.

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

### Phase 5: Spawn Workers

Use these plugin subagents:

- `go-review:go-review-worker`
- `go-review:go-review-dedup-judge`
- `go-review:go-review-fp-judge`

Use the same worker protocol as `c-review` and `rust-review`:

- optional foreground cache primer
- workers spawned foreground in waves of at most 16
- no `run_in_background=true`
- pass each rendered worker prompt verbatim
- each worker writes findings, shard, and coverage artifacts
- use the requested `worker_model` for every worker and the primer

### Phase 6: Validate Worker Artifacts

For each completed worker, run:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/validate_artifacts.py" \
  "${output_dir}/plan.json" \
  --worker "worker-N" \
  --claimed-count "worker-N=<count>"
```

After all workers complete, build `findings-index.txt` from the union of worker
shards and reconcile it against `findings/*.md`. Keep orphan findings in the
index and record incomplete shards in `run-summary.md`; do not silently drop a
finding because a worker crashed after writing it.

### Phase 7: Judges and Reports

Run `go-review:go-review-dedup-judge`, then
`go-review:go-review-fp-judge`, each with `output_dir` in the prompt. The FP
judge also receives the absolute path to [generate_sarif.py](../../scripts/generate_sarif.py).

Always run the SARIF safety net:

```sh
python3 "${GO_REVIEW_PLUGIN_ROOT}/scripts/generate_sarif.py" "${output_dir}"
```

Return `REPORT.md`, `REPORT.sarif`, `go-inventory.json`, and `run-summary.md`.

## Success Criteria

- `go-inventory.json` exists and reports a service surface
- every planned worker has a coverage file and shard
- `findings-index.txt` exists even for zero findings
- `dedup-summary.md`, `fp-summary.md`, `REPORT.md`, and `REPORT.sarif` exist
- any truncated or failed worker is surfaced in `run-summary.md`
