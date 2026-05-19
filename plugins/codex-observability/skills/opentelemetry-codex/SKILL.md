---
name: opentelemetry-codex
description: Install and configure OpenTelemetry for Codex-oriented workflows, including OTLP exporter setup, collector endpoint wiring, and validation that traces/logs/metrics are emitted and stored under PROJECT_PATH/OpenTelemetry.
---

# OpenTelemetry Codex

Use this skill when the operator asks to add OpenTelemetry (OTEL) instrumentation or telemetry export for Codex workflows in a repository.
Direct trigger phrase: `Install OpenTelemetry`.

## Input Contract

Accept input as: `PROJECT_PATH OTLP_ENDPOINT MODE`

Mode:
- `plan`: produce an implementation plan only
- `execute` (default): apply configuration and validate telemetry emission

Examples:
- `$opentelemetry-codex /path/to/repo http://127.0.0.1:4318 execute`
- `$opentelemetry-codex /path/to/repo https://otel-collector.internal:4318 plan`

## Preconditions

1. Confirm the target project is in scope for modification.
2. Detect project runtime/language before choosing instrumentation package(s).
3. Confirm an OTLP endpoint exists (collector or vendor gateway).
4. Configure Codex OTEL via `config.toml` blocks, not shell env vars.
5. Default local telemetry storage path is `PROJECT_PATH/OpenTelemetry`.

## Execution Workflow

1. Baseline inventory:
- detect primary runtime and dependency manager,
- identify existing telemetry/logging framework.
- if `PROJECT_PATH/OpenTelemetry/install_opentelemetry.sh` exists, prefer it as the default implementation path for consistency across clones.

2. Configure Codex OTEL in `config.toml`:
- `[otel]`
- `service_name = "codex-agent"` (or project-specific service name)
- `log_user_prompt = true` (when operator wants prompt logging)
- `exporter = "otlp-http"`
- `[otel.exporter."otlp-http"]`
- `endpoint = "<OTLP_ENDPOINT>"`
- `protocol = "json"` (use `binary` when compact transport is preferred)
- Use supported exporter variants (`otlp-http`, `otlp-grpc`, `statsig`, `none`) and valid protocol values when applicable.
- Do not rely on `OTEL_*` shell environment variables for primary wiring.

3. Install/Bootstrap (preferred path):
- run `"$PROJECT_PATH/OpenTelemetry/install_opentelemetry.sh"` when available.
- this should prepare the local runtime and ensure telemetry output files exist.

4. Add startup wiring so telemetry initializes at process start.
- default runner should be `"$PROJECT_PATH/OpenTelemetry/run_codex_with_otel.sh"` for user-friendly operation.
- when using an OpenTelemetry Collector, configure a `file` exporter writing to:
  - `"$PROJECT_PATH/OpenTelemetry/otel-logs.jsonl"`
  - `"$PROJECT_PATH/OpenTelemetry/otel-traces.jsonl"` (if traces are persisted locally)

5. Add a minimal smoke operation that should emit telemetry (single request/task run).

6. Validate:
- process starts successfully,
- OTEL exporter attempts/acknowledges delivery,
- collector/backend receives signal data (trace/log/metric as available).
- local files under `"$PROJECT_PATH/OpenTelemetry"` are created and non-empty when file export is enabled.

7. Document exact run commands and outputs for reproducibility.

## Codex Data Capture Guidance

When instrumenting Codex workflows, capture at least:
- command execution lifecycle (start/end/error),
- task identifiers and branch/repo context,
- high-level agent role labels (`planner`, `researcher`, etc.),
- latency and status outcomes.

Do not export secrets, raw credentials, or full sensitive payloads in spans/logs.
Use redaction or attribute allow-lists for safety.

## Reporting Requirements

For each implementation, include:
- runtime and OTEL package(s) installed,
- exact config changes (file paths and `config.toml` OTEL blocks),
- local storage path used: `PROJECT_PATH/OpenTelemetry`,
- verification commands and resulting output,
- timestamp (UTC ISO 8601),
- confirmed telemetry signals observed,
- follow-up hardening recommendations.
