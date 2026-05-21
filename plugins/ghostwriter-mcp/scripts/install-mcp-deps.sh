#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_dir="$(cd "${script_dir}/.." && pwd)"

source_ref="${GHOSTWRITER_MCP_SOURCE:-}"
target_dir="${GHOSTWRITER_MCP_DIR:-${plugin_dir}/vendor/ghostwriter-mcp}"
run_uv_sync="${GHOSTWRITER_MCP_UV_SYNC:-1}"

usage() {
  cat <<'EOF'
Usage: install-mcp-deps.sh --source <git-url-or-local-path> [options]

Installs the Ghostwriter MCP server next to the ghostwriter-mcp plugin.

Options:
  --source <git-url-or-local-path>  Override GHOSTWRITER_MCP_SOURCE
  --target <path>                   Override GHOSTWRITER_MCP_DIR
  --no-uv-sync                      Clone/copy only; skip uv sync
  -h, --help

Environment:
  GHOSTWRITER_MCP_SOURCE            Git URL or local checkout/source path
  GHOSTWRITER_MCP_DIR               Target install directory
  GHOSTWRITER_MCP_UV_SYNC=0         Skip uv sync
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

if [[ -z "${source_ref}" ]]; then
  echo "GHOSTWRITER_MCP_SOURCE or --source is required; no canonical Ghostwriter MCP source is bundled in this repo." >&2
  usage >&2
  exit 2
fi

mkdir -p "$(dirname "${target_dir}")"

if [[ -d "${target_dir}/.git" ]]; then
  echo "Updating Ghostwriter MCP checkout at ${target_dir}"
  git -C "${target_dir}" pull --ff-only
elif [[ -e "${target_dir}" ]]; then
  echo "Target exists but is not a git checkout: ${target_dir}" >&2
  echo "Move it aside or set GHOSTWRITER_MCP_DIR to a different path." >&2
  exit 1
elif [[ -d "${source_ref}" && ! -d "${source_ref}/.git" ]]; then
  echo "Copying Ghostwriter MCP source from ${source_ref} to ${target_dir}"
  mkdir -p "${target_dir}"
  cp -a "${source_ref}/." "${target_dir}/"
else
  echo "Installing Ghostwriter MCP from ${source_ref} to ${target_dir}"
  git clone "${source_ref}" "${target_dir}"
fi

if [[ "${run_uv_sync}" != "0" ]]; then
  if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required to sync Ghostwriter MCP dependencies. Install uv or rerun with --no-uv-sync." >&2
    exit 1
  fi
  echo "Syncing Ghostwriter MCP dependencies with uv"
  (cd "${target_dir}" && uv sync)
fi

cat <<EOF
Ghostwriter MCP installed.

Server directory:
  ${target_dir}

Codex MCP runner:
  ${plugin_dir}/scripts/run-ghostwriter-mcp.sh

Runtime configuration:
  Provide GHOSTWRITER_URL, GHOSTWRITER_API_KEY, and optionally GHOSTWRITER_CA_BUNDLE
  through your Codex environment or shell environment before starting Codex.
EOF
