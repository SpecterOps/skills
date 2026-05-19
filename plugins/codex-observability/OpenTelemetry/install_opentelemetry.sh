#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_FILE="${PROJECT_DIR}/config.toml"
PYTHON_BIN="${SCRIPT_DIR}/.venv/bin/python"

if ! command -v python3 >/dev/null 2>&1; then
  echo "missing_python3" >&2
  exit 1
fi

mkdir -p "${SCRIPT_DIR}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${SCRIPT_DIR}/.venv"
  echo "created_venv path=${SCRIPT_DIR}/.venv"
else
  echo "venv_exists path=${SCRIPT_DIR}/.venv"
fi

touch "${SCRIPT_DIR}/otel-logs.jsonl" "${SCRIPT_DIR}/otel-traces.jsonl"
echo "ensured_files ${SCRIPT_DIR}/otel-logs.jsonl ${SCRIPT_DIR}/otel-traces.jsonl"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "missing_config_toml ${CONFIG_FILE}" >&2
  exit 1
fi

if grep -q '^\[otel\]' "${CONFIG_FILE}" \
  && grep -Eq '^[[:space:]]*exporter[[:space:]]*=[[:space:]]*\{.*otlp-http.*\}[[:space:]]*$' "${CONFIG_FILE}"; then
  echo "config_present file=${CONFIG_FILE}"
else
  if grep -q '^\[otel\]' "${CONFIG_FILE}"; then
    tmp_config="$(mktemp)"
    awk '
      /^\[otel\]$/ {skip=1; next}
      skip == 1 && /^\[/ && $0 !~ /^\[otel(\.|])/ {skip=0}
      skip == 0 {print}
    ' "${CONFIG_FILE}" > "${tmp_config}"
    mv "${tmp_config}" "${CONFIG_FILE}"
    echo "config_migrated_removed_legacy_otel file=${CONFIG_FILE}"
  fi

  cat >>"${CONFIG_FILE}" <<'EOF'

[otel]
service_name = "codex-agent"
log_user_prompt = true
exporter = { "otlp-http" = { endpoint = "http://127.0.0.1:4318", protocol = "json" } }
EOF
  echo "config_appended file=${CONFIG_FILE}"
fi

echo "install_complete"
echo "next_step ./OpenTelemetry/run_codex_with_otel.sh"
