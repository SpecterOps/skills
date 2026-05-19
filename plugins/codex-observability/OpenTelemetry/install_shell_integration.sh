#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="${SCRIPT_DIR}/run_codex_with_otel.sh"
TARGET_RC="${HOME}/.zshrc"
BEGIN_MARKER="# >>> CODEX OTEL INTEGRATION >>>"
END_MARKER="# <<< CODEX OTEL INTEGRATION <<<"
MAKE_DEFAULT=0

usage() {
  cat <<'EOF'
Usage:
  ./OpenTelemetry/install_shell_integration.sh [--make-default]

Options:
  --make-default   Alias `codex` to run with OTEL.
                   Without this option, only `codex-otel` is added.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --make-default)
      MAKE_DEFAULT=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown_argument $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! -x "${WRAPPER}" ]]; then
  echo "wrapper_not_executable ${WRAPPER}" >&2
  exit 1
fi

tmp_file="$(mktemp)"
if [[ -f "${TARGET_RC}" ]]; then
  awk -v begin="${BEGIN_MARKER}" -v end="${END_MARKER}" '
    $0 == begin {skip=1; next}
    $0 == end {skip=0; next}
    skip == 0 {print}
  ' "${TARGET_RC}" > "${tmp_file}"
fi

{
  cat "${tmp_file}"
  echo "${BEGIN_MARKER}"
  echo "alias codex-otel='${WRAPPER}'"
  if [[ ${MAKE_DEFAULT} -eq 1 ]]; then
    echo "alias codex='${WRAPPER}'"
    echo "mode: default_codex_uses_otel"
  else
    echo "mode: codex_unchanged_plus_codex-otel_alias"
  fi
  echo "${END_MARKER}"
} > "${TARGET_RC}"

rm -f "${tmp_file}"

echo "shell_integration_installed file=${TARGET_RC}"
echo "reload_hint source ${TARGET_RC}"
