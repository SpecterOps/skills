#!/usr/bin/env bash
set -euo pipefail

config_file=${1:-local-harnesses/build.config.json}

command -v jq >/dev/null || {
  printf 'error: jq is required\n' >&2
  exit 1
}
[[ -f $config_file ]] || {
  printf 'error: BHE build config not found: %s\n' "$config_file" >&2
  exit 1
}

tmp_file=$(mktemp "${config_file}.tmp.XXXXXX")
trap 'rm -f "$tmp_file"' EXIT

jq '.default_admin.email_address = "admin@example.com" |
    .default_admin.password = "ChangeMe123!" |
    .default_admin.expire_now = false' \
  "$config_file" > "$tmp_file"

mv "$tmp_file" "$config_file"
trap - EXIT

printf 'Configured local BHE administrator: admin@example.com\n'
