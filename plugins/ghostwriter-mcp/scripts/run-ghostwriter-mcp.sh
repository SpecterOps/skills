#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_dir="$(cd "${script_dir}/.." && pwd)"
server_dir="${GHOSTWRITER_MCP_DIR:-${plugin_dir}/vendor/ghostwriter-mcp}"

if [[ ! -d "${server_dir}" ]]; then
  cat >&2 <<EOF
Ghostwriter MCP is not installed at:
  ${server_dir}

Install it alongside the plugin with:
  GHOSTWRITER_MCP_SOURCE=<git-url-or-local-path> ${plugin_dir}/scripts/install-mcp-deps.sh

Or set GHOSTWRITER_MCP_DIR to an existing Ghostwriter MCP server checkout.
EOF
  exit 127
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to run Ghostwriter MCP." >&2
  exit 127
fi

exec uv --directory "${server_dir}" run python -m ghostwritermcp.server
