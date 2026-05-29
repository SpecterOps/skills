#!/usr/bin/env bash
set -euo pipefail

config_path="${1:?usage: run_stage3_stub.sh <course-config> [qa-mode] [preview-url]}"
qa_mode="${2:-local}"
preview_url="${3:-}"

printf '== Stage 3 QA And Targeted Polish ==\n'
printf 'qa_mode=%s\n' "$qa_mode"

case "$qa_mode" in
  local)
    echo "Expected browser target: local Hugo pcode-review"
    ;;
  deployed)
    if [[ -z "$preview_url" ]]; then
      echo "Preview URL is required for deployed QA mode" >&2
      exit 1
    fi
    printf 'preview_url=%s\n' "$preview_url"
    ;;
  both)
    if [[ -z "$preview_url" ]]; then
      echo "Preview URL is required for QA mode both" >&2
      exit 1
    fi
    printf 'preview_url=%s\n' "$preview_url"
    echo "Expected browser targets: local preview and deployed pcode-review"
    ;;
  *)
    echo "Unsupported qa_mode: $qa_mode" >&2
    exit 1
    ;;
esac

cat <<'EOF'
Stage 3 expectations:
- run representative browser checks
- run a full derived-route sweep
- compare presentation to the template shell without flattening original course content
- apply one bounded rendering-only polish pass
- rerun build and affected browser checks

QA findings should be grouped by:
- navigation
- broken assets
- PDF rendering
- layout or spacing mismatches
- content placement issues

Also report:
- acceptable intentional differences from the template shell
- full route sweep summary
- post-fix validation status
- residual risks
EOF
