#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/common.sh"

config_path="${1:?usage: run_stage2.sh <course-config> [qa-mode] [git-mode]}"
qa_mode="${2:-local}"
git_mode="${3:-auto}"

print_stage_header "Stage 2 Preflight"

legacy_content="$(require_cfg "$config_path" legacy_participant_content)"
legacy_root="$(require_cfg "$config_path" legacy_course_root)"
target_repo="$(require_cfg "$config_path" target_repo)"

require_path "legacy_participant_content" "$legacy_content"
require_path "legacy_course_root" "$legacy_root"
require_path "target_repo" "$target_repo"

echo "legacy_content=$legacy_content"
echo "legacy_root=$legacy_root"
echo "target_repo=$target_repo"
echo "qa_mode=$qa_mode"
echo "git_mode=$git_mode"

print_stage_header "Stage 2 Expected Checks"
echo "- legacy course repo hydrated with git lfs pull before copy when applicable"
echo "- legacy participant content copied into target repo"
echo "- content text preserved while rendering is converted"
echo "- unresolved Git LFS pointers reported before build"
echo "- local Hugo build passes"
echo "- representative lab, resource, slide, PDF, and image pages are ready for browser QA"

print_stage_header "Legacy Source Hydration"
if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  git -C "$legacy_root" lfs install
  git -C "$legacy_root" lfs pull
  echo "Legacy source hydration complete"
else
  echo "git-lfs is required to hydrate the legacy course repo before stage 2 import" >&2
  exit 1
fi

print_stage_header "Legacy Source LFS Pointers"
if ! rg -n "git-lfs.github.com/spec/v1" "$legacy_content"; then
  echo "No unresolved LFS pointers found in legacy participant content"
fi

print_stage_header "Unresolved LFS Pointers"
if ! rg -n "git-lfs.github.com/spec/v1" "$target_repo/content"; then
  echo "No unresolved LFS pointers found under content"
fi

if [[ "$git_mode" == "auto" ]]; then
  print_stage_header "Git Status"
  git_summary "$target_repo"
fi
