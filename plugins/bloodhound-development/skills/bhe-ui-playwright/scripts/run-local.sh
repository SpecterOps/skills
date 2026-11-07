#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: BHE_PASSWORD=<password> $0 <local-bhe-url> [playwright-args...]" >&2
    exit 2
fi

target_url="$1"
shift

if [[ ! "$target_url" =~ ^https?://(localhost|127\.0\.0\.1|([a-zA-Z0-9-]+\.)+localhost)(:[0-9]+)?(/.*)?$ ]]; then
    echo "Refusing to send local BHE credentials to a non-local URL: $target_url" >&2
    exit 2
fi

: "${BHE_PASSWORD:?Set BHE_PASSWORD for the local development account}"

harness_dir="${BHE_PLAYWRIGHT_HARNESS:-$HOME/Documents/codex/experiments/bhe-playwright-pilot}"
username="${BHE_USERNAME:-admin@example.com}"

if [[ ! -f "$harness_dir/package.json" ]]; then
    echo "Playwright harness not found at: $harness_dir" >&2
    exit 2
fi

(
    cd "$harness_dir"
    BHE_URL="$target_url" BHE_USERNAME="$username" BHE_PASSWORD="$BHE_PASSWORD" npm test -- "$@"
)
