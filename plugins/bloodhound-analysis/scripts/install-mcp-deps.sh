#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_dir="$(cd "${script_dir}/.." && pwd)"

source_ref="${BLOODHOUND_MCP_SOURCE:-https://github.com/mwnickerson/bloodhound_mcp.git}"
target_dir="${BLOODHOUND_MCP_DIR:-${plugin_dir}/vendor/bloodhound-mcp}"
run_uv_sync="${BLOODHOUND_MCP_UV_SYNC:-1}"

usage() {
  cat <<'EOF'
Usage: install-mcp-deps.sh [options]

Installs the BloodHound MCP server next to the bloodhound-analysis plugin.

Options:
  --source <git-url-or-local-path>  Override BLOODHOUND_MCP_SOURCE
  --target <path>                   Override BLOODHOUND_MCP_DIR
  --no-uv-sync                      Clone/copy only; skip uv sync
  -h, --help

Environment:
  BLOODHOUND_MCP_SOURCE             Git URL or local checkout path
  BLOODHOUND_MCP_DIR                Target install directory
  BLOODHOUND_MCP_UV_SYNC=0          Skip uv sync
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_ref="${2:?missing source value}"
      shift 2
      ;;
    --target)
      target_dir="${2:?missing target value}"
      shift 2
      ;;
    --no-uv-sync)
      run_uv_sync=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "$(dirname "${target_dir}")"

if [[ -d "${target_dir}/.git" ]]; then
  echo "Updating BloodHound MCP checkout at ${target_dir}"
  git -C "${target_dir}" pull --ff-only
elif [[ -e "${target_dir}" ]]; then
  echo "Target exists but is not a git checkout: ${target_dir}" >&2
  echo "Move it aside or set BLOODHOUND_MCP_DIR to a different path." >&2
  exit 1
else
  echo "Installing BloodHound MCP from ${source_ref} to ${target_dir}"
  git clone "${source_ref}" "${target_dir}"
fi

if [[ "${run_uv_sync}" != "0" ]]; then
  if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required to sync BloodHound MCP dependencies. Install uv or rerun with --no-uv-sync." >&2
    exit 1
  fi
  echo "Syncing BloodHound MCP dependencies with uv"
  (cd "${target_dir}" && uv sync)
fi

cat <<EOF
BloodHound MCP installed.

Server directory:
  ${target_dir}

Codex MCP runner:
  ${plugin_dir}/scripts/run-bloodhound-mcp.sh

Credential setup:
  Copy ${plugin_dir}/mcp/env.example to ${target_dir}/.env and fill in BloodHound values,
  or provide the BLOODHOUND_* variables through your local environment/config.
EOF
