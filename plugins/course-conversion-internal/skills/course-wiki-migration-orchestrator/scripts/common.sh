#!/usr/bin/env bash
set -euo pipefail

cfg_get() {
  local config_path="$1"
  local key_path="$2"
  python3 - "$config_path" "$key_path" <<'PY'
import sys
from pathlib import Path
import yaml

config_path = Path(sys.argv[1])
key_path = sys.argv[2].split(".")

with config_path.open("r", encoding="utf-8") as handle:
    data = yaml.safe_load(handle) or {}

value = data
for key in key_path:
    if not isinstance(value, dict) or key not in value:
        sys.exit(1)
    value = value[key]

if isinstance(value, bool):
    print("true" if value else "false")
elif value is None:
    print("")
else:
    print(value)
PY
}

require_cfg() {
  local config_path="$1"
  local key_path="$2"
  local value
  if ! value="$(cfg_get "$config_path" "$key_path" 2>/dev/null)"; then
    echo "Missing required config key: $key_path" >&2
    return 1
  fi
  if [[ -z "$value" ]]; then
    echo "Empty required config key: $key_path" >&2
    return 1
  fi
  printf '%s\n' "$value"
}

require_path() {
  local label="$1"
  local path_value="$2"
  if [[ ! -e "$path_value" ]]; then
    echo "Missing path for $label: $path_value" >&2
    return 1
  fi
}

git_summary() {
  local repo_path="$1"
  git -C "$repo_path" status --short --branch
}

print_stage_header() {
  local stage_name="$1"
  printf '\n== %s ==\n' "$stage_name"
}
