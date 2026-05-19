#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${SCRIPT_DIR}/otlp_receiver.pid"
OUT_FILE="${SCRIPT_DIR}/otlp_receiver.out"
PYTHON_BIN="${SCRIPT_DIR}/.venv/bin/python"
RECEIVER_SCRIPT="${SCRIPT_DIR}/otlp_file_receiver.py"

ensure_python_venv() {
  if [[ -x "${PYTHON_BIN}" ]]; then
    return 0
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "missing_python3" >&2
    return 1
  fi

  python3 -m venv "${SCRIPT_DIR}/.venv"
}

if [[ ! -f "${RECEIVER_SCRIPT}" ]]; then
  echo "missing_receiver_script: ${RECEIVER_SCRIPT}" >&2
  exit 1
fi

if [[ -f "${PID_FILE}" ]]; then
  pid="$(cat "${PID_FILE}")"
  if kill -0 "${pid}" 2>/dev/null; then
    echo "receiver_already_running pid=${pid}"
    exit 0
  fi
  rm -f "${PID_FILE}"
fi

ensure_python_venv
nohup "${PYTHON_BIN}" "${RECEIVER_SCRIPT}" >>"${OUT_FILE}" 2>&1 &
pid=$!
echo "${pid}" > "${PID_FILE}"
sleep 0.2
if ! kill -0 "${pid}" 2>/dev/null; then
  echo "receiver_failed_to_start" >&2
  tail -n 20 "${OUT_FILE}" >&2 || true
  rm -f "${PID_FILE}"
  exit 1
fi
echo "receiver_started pid=${pid} out=${OUT_FILE}"
