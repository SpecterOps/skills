#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_dir="$(cd "${script_dir}/.." && pwd)"
server_dir="${BLOODHOUND_MCP_DIR:-${plugin_dir}/vendor/bloodhound-mcp}"

if [[ ! -f "${server_dir}/main.py" ]]; then
  cat >&2 <<EOF
BloodHound MCP is not installed at:
  ${server_dir}

Install it alongside the plugin with:
  ${plugin_dir}/scripts/install-mcp-deps.sh

Or set BLOODHOUND_MCP_DIR to an existing bloodhound_mcp checkout.
EOF
  exit 127
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to run BloodHound MCP." >&2
  exit 127
fi

exec uv --directory "${server_dir}" run main.py
