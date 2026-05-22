#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_dir="$(cd "${script_dir}/.." && pwd)"
server_dir="${GHOSTWRITER_MCP_DIR:-${plugin_dir}/vendor/ghostwriter-mcp}"

if [[ ! -d "${server_dir}" ]]; then
  if [[ "${GHOSTWRITER_MCP_AUTO_INSTALL:-1}" != "0" ]]; then
    echo "Ghostwriter MCP is not installed at ${server_dir}; installing plugin-local dependency..." >&2
    "${script_dir}/install-ghostwriter-mcp-deps.sh" >&2
  fi
fi

if [[ ! -d "${server_dir}" ]]; then
  cat >&2 <<EOF
Ghostwriter MCP is not installed at:
  ${server_dir}

Auto-install did not complete. Install it with:
  ${plugin_dir}/scripts/install-ghostwriter-mcp-deps.sh

Or set GHOSTWRITER_MCP_DIR to an existing Ghostwriter MCP server checkout.
Set GHOSTWRITER_MCP_AUTO_INSTALL=0 to disable first-run auto-install.
EOF
  exit 127
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to run Ghostwriter MCP." >&2
  exit 127
fi

exec uv --directory "${server_dir}" run python -m ghostwritermcp.server
