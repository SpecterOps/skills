# Codex + OpenTelemetry Setup

This directory provides a local OTLP receiver for validating Codex telemetry in this repo.

## What This Gives You

- `start_otlp_receiver.sh`: starts a local OTLP HTTP receiver at `127.0.0.1:4318`.
- `stop_otlp_receiver.sh`: stops the local receiver.
- `otlp_file_receiver.py`: writes incoming telemetry to local JSONL files.
- `install_opentelemetry.sh`: one-time bootstrap (venv + log files + OTEL config check).
- `run_codex_with_otel.sh`: runs Codex with the OTLP receiver for that session.
- `install_shell_integration.sh`: adds shell aliases (optional).

## Quick Start

1. Install/bootstrap once:

```bash
./OpenTelemetry/install_opentelemetry.sh
```

2. Run Codex with OTEL for a session:

```bash
./OpenTelemetry/run_codex_with_otel.sh
```

This wrapper injects OTEL settings via `codex -c ...`, so it does not depend on `~/.codex/config.toml`.
It uses the OTEL keys accepted by Codex `v0.107.x` and enables
`otel.log_user_prompt=true`.

3. Optional: add a reusable alias:

```bash
./OpenTelemetry/install_shell_integration.sh
source ~/.zshrc
codex-otel
```

If you want `codex` itself to always use OTEL:

```bash
./OpenTelemetry/install_shell_integration.sh --make-default
source ~/.zshrc
```

## Files You Can Customize

- `otlp_file_receiver.py`: local receiver implementation writing `otel-logs.jsonl` and `otel-traces.jsonl`.

## Config Shape Used (Docs-Aligned)

```toml
[otel]
service_name = "codex-agent"
log_user_prompt = true
exporter = { "otlp-http" = { endpoint = "http://127.0.0.1:4318", protocol = "json" } }
```

## Output Artifacts

- `OpenTelemetry/otel-logs.jsonl`
- `OpenTelemetry/otel-traces.jsonl`
- `OpenTelemetry/otlp_receiver.out`
