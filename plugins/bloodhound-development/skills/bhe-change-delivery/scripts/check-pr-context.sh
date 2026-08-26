#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

for dependency in git gh jq; do
  command -v "$dependency" >/dev/null 2>&1 ||
    die "missing required command: $dependency"
done

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) ||
  die "run inside the repository that will receive the pull request"
branch=$(git -C "$repo_root" branch --show-current)
[[ -n $branch ]] || die "the repository is on a detached HEAD"

remote_url=$(git -C "$repo_root" remote get-url origin 2>/dev/null) ||
  die "the repository has no origin remote"
repo_json=$(gh repo view --json nameWithOwner,visibility,defaultBranchRef 2>/dev/null) ||
  die "could not resolve GitHub repository metadata for $remote_url"

repo_name=$(jq -r '.nameWithOwner // empty' <<< "$repo_json")
visibility=$(jq -r '.visibility // empty | ascii_upcase' <<< "$repo_json")
default_branch=$(jq -r '.defaultBranchRef.name // empty' <<< "$repo_json")
[[ -n $repo_name ]] || die "GitHub metadata did not include nameWithOwner"
case "$visibility" in
  PUBLIC|PRIVATE|INTERNAL) ;;
  *) die "GitHub metadata returned an unsupported visibility: ${visibility:-empty}" ;;
esac
[[ -n $default_branch ]] || die "GitHub metadata did not include a default branch"

upstream=$(git -C "$repo_root" rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || true)
already_pushed=false
if [[ -n $upstream ]]; then
  git -C "$repo_root" merge-base --is-ancestor HEAD "$upstream" &&
    already_pushed=true
elif git -C "$repo_root" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
  git -C "$repo_root" merge-base --is-ancestor HEAD "origin/$branch" &&
    already_pushed=true
fi

working_tree_clean=true
[[ -z $(git -C "$repo_root" status --porcelain=v1) ]] || working_tree_clean=false

jq -n \
  --arg repo "$repo_name" \
  --arg visibility "$visibility" \
  --arg root "$repo_root" \
  --arg remote_url "$remote_url" \
  --arg branch "$branch" \
  --arg upstream "$upstream" \
  --arg default_branch "$default_branch" \
  --argjson already_pushed "$already_pushed" \
  --argjson working_tree_clean "$working_tree_clean" \
  '{repo:$repo, visibility:$visibility, root:$root, remote_url:$remote_url,
    branch:$branch, upstream:($upstream | if length == 0 then null else . end),
    already_pushed:$already_pushed, default_branch:$default_branch,
    working_tree_clean:$working_tree_clean}'
