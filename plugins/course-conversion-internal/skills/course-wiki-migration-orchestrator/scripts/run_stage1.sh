#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/common.sh"

config_path="${1:?usage: run_stage1.sh <course-config> [qa-mode] [git-mode]}"
qa_mode="${2:-local}"
git_mode="${3:-auto}"

print_stage_header "Stage 1 Preflight"

source_repo="$(require_cfg "$config_path" source_scaffold_repo)"
target_repo="$(require_cfg "$config_path" target_repo)"
target_branch="$(require_cfg "$config_path" target_branch)"
course_title="$(require_cfg "$config_path" course_title)"

require_path "source_scaffold_repo" "$source_repo"
require_path "target_repo" "$target_repo"

echo "course_title=$course_title"
echo "source_repo=$source_repo"
echo "target_repo=$target_repo"
echo "target_branch=$target_branch"
echo "qa_mode=$qa_mode"
echo "git_mode=$git_mode"

print_stage_header "Stage 1 Expected Checks"
echo "- scaffold copied from the configured template repo excluding .git and source content"
echo "- hugo.yaml and README.md updated for course identity"
echo "- amplify.yml and buildspec.yml contain Git LFS install/pull steps"
echo "- minimal content shell exists"
echo "- local Hugo build passes before push"

if [[ "$git_mode" == "auto" ]]; then
  print_stage_header "Git Status"
  git_summary "$target_repo"
fi
