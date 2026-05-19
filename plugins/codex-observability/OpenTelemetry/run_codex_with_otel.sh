#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_SCRIPT="${SCRIPT_DIR}/start_otlp_receiver.sh"
STOP_SCRIPT="${SCRIPT_DIR}/stop_otlp_receiver.sh"

if ! command -v codex >/dev/null 2>&1; then
  echo "missing_codex_binary" >&2
  exit 1
fi

start_out="$("${START_SCRIPT}")"
echo "${start_out}"
started_here=0
if [[ "${start_out}" == receiver_started* ]]; then
  started_here=1
fi

set +e
codex \
  -c 'otel.service_name="codex-agent"' \
  -c 'otel.log_user_prompt=true' \
  -c 'otel.exporter={"otlp-http"={endpoint="http://127.0.0.1:4318",protocol="json"}}' \
  "$@"
codex_rc=$?
set -e

if [[ ${started_here} -eq 1 ]]; then
  "${STOP_SCRIPT}" >/dev/null 2>&1 || true
fi

exit "${codex_rc}"
