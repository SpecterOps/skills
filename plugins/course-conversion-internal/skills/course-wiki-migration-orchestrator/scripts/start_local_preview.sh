#!/usr/bin/env bash
set -euo pipefail

repo_path="${1:?usage: start_local_preview.sh <target-repo> [bind] [port]}"
bind_addr="${2:-127.0.0.1}"
port="${3:-1313}"

pick_hugo_bin() {
  if [[ -n "${HUGO_BIN:-}" && -x "${HUGO_BIN}" ]]; then
    printf '%s
' "${HUGO_BIN}"
    return 0
  fi

  if [[ -x "/tmp/course-tools/hugo/hugo" ]]; then
    printf '%s
' "/tmp/course-tools/hugo/hugo"
    return 0
  fi

  if command -v hugo >/dev/null 2>&1; then
    command -v hugo
    return 0
  fi

  return 1
}

if ! hugo_bin="$(pick_hugo_bin)"; then
  echo "a compatible Hugo binary is required to start a local pcode-review" >&2
  exit 1
fi

cd "$repo_path"
nohup "$hugo_bin" server --bind "$bind_addr" --baseURL "http://$bind_addr:$port" --port "$port" --disableFastRender >/tmp/course-wiki-hugo.log 2>&1 &
server_pid=$!
echo "$server_pid"
echo "http://$bind_addr:$port"
echo "$hugo_bin"
