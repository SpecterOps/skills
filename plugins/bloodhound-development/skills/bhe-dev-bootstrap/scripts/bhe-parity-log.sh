#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage:' \
    '  bhe-parity-log.sh init --task SLUG --repo PATH' \
    '  bhe-parity-log.sh record --task SLUG --change-id SLUG --change TEXT --surface SURFACE' \
    '      --disposition DISPOSITION --reason TEXT --bhe-validation TEXT' \
    '      --bhce-validation TEXT --follow-up TEXT [--bhe-ref TEXT] [--bhce-ref TEXT]' \
    '  bhe-parity-log.sh show --task SLUG' \
    '  bhe-parity-log.sh check --task SLUG [--stage iteration|pr]' \
    '  bhe-parity-log.sh archive --task SLUG' \
    '  bhe-parity-log.sh list'
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

one_line() {
  local value=$1
  value=${value//$'\r'/ }
  value=${value//$'\n'/ }
  printf '%s' "$value"
}

validate_slug() {
  local label=$1
  local value=$2
  [[ $value =~ ^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$ || $value =~ ^[a-z0-9]$ ]] ||
    die "$label must be a lowercase slug of 1-64 characters"
}

ensure_root() {
  mkdir -p "$entries_dir"
  chmod 700 "$state_root" "$entries_dir"
}

command_name=${1:-}
case "$command_name" in
  init|record|show|check|archive|list) shift ;;
  -h|--help|'') usage; exit 0 ;;
  *) usage >&2; die "unknown command: $command_name" ;;
esac

task=
repo=
change_id=
change=
surface=
disposition=
reason=
bhe_validation=
bhce_validation=
follow_up=
bhe_ref=pending
bhce_ref=none
stage=pr

while (($#)); do
  case "$1" in
    --task) task=${2:-}; shift 2 ;;
    --repo) repo=${2:-}; shift 2 ;;
    --change-id) change_id=${2:-}; shift 2 ;;
    --change) change=${2:-}; shift 2 ;;
    --surface) surface=${2:-}; shift 2 ;;
    --disposition) disposition=${2:-}; shift 2 ;;
    --reason) reason=${2:-}; shift 2 ;;
    --bhe-validation) bhe_validation=${2:-}; shift 2 ;;
    --bhce-validation) bhce_validation=${2:-}; shift 2 ;;
    --follow-up) follow_up=${2:-}; shift 2 ;;
    --bhe-ref) bhe_ref=${2:-}; shift 2 ;;
    --bhce-ref) bhce_ref=${2:-}; shift 2 ;;
    --stage) stage=${2:-}; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

state_root=${BHE_PARITY_STATE_ROOT:-${XDG_STATE_HOME:-$HOME/.local/state}/codex-bhe-parity}
entries_dir=$state_root/entries
ensure_root

if [[ $command_name == list ]]; then
  found=false
  for entry_file in "$entries_dir"/*.md; do
    [[ -f $entry_file ]] || continue
    found=true
    entry_task=$(basename "$entry_file" .md)
    recorded_repo=$(sed -n 's/^- Worktree: //p' "$entry_file" | head -1)
    printf '%s\t%s\t%s\n' "$entry_task" "$recorded_repo" "$entry_file"
  done
  $found || printf 'No BHE/BHCE parity entries under %s\n' "$entries_dir"
  exit 0
fi

[[ -n $task ]] || die "--task is required"
validate_slug "--task" "$task"
entry_file=$entries_dir/$task.md

if [[ $command_name != check && $stage != pr ]]; then
  die "--stage is valid only with check"
fi
case "$stage" in
  iteration|pr) ;;
  *) die "--stage must be iteration or pr" ;;
esac

if [[ $command_name == init ]]; then
  [[ -n $repo ]] || die "--repo is required"
  [[ -d $repo ]] || die "worktree does not exist: $repo"
  repo=$(cd "$repo" && pwd -P)
  branch=$(git -C "$repo" branch --show-current 2>/dev/null || true)
  [[ -n $branch ]] || branch=detached-or-unknown

  if [[ -f $entry_file ]]; then
    recorded_repo=$(sed -n 's/^- Worktree: //p' "$entry_file" | head -1)
    [[ $recorded_repo == "$repo" ]] ||
      die "task '$task' already belongs to another worktree: $recorded_repo"
    printf 'Parity ledger already initialized: %s\n' "$entry_file"
    exit 0
  fi

  started=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  printf '# BHE/BHCE Delta: %s\n\n- Worktree: %s\n- Branch: %s\n- Started: %s\n' \
    "$task" "$repo" "$branch" "$started" > "$entry_file"
  chmod 600 "$entry_file"
  printf 'Initialized parity ledger: %s\n' "$entry_file"
  exit 0
fi

[[ -f $entry_file ]] || die "task '$task' is not initialized; run init first"

if [[ $command_name == show ]]; then
  printf 'Parity ledger: %s\n\n' "$entry_file"
  sed -n '1,$p' "$entry_file"
  exit 0
fi

if [[ $command_name == archive ]]; then
  [[ ! -d $entry_file.lock ]] ||
    die "cannot archive while another process may be updating $entry_file"
  archive_dir=$state_root/archive
  mkdir -p "$archive_dir"
  archived_at=$(date -u '+%Y%m%dT%H%M%SZ')
  archive_file=$archive_dir/$task-$archived_at.md
  [[ ! -e $archive_file ]] || die "archive target already exists: $archive_file"
  mv "$entry_file" "$archive_file"
  chmod 600 "$archive_file"
  printf 'Archived parity ledger: %s\n' "$archive_file"
  exit 0
fi

if [[ $command_name == check ]]; then
  recorded_repo=$(sed -n 's/^- Worktree: //p' "$entry_file" | head -1)
  recorded_branch=$(sed -n 's/^- Branch: //p' "$entry_file" | head -1)
  [[ -d $recorded_repo ]] || die "recorded worktree no longer exists: $recorded_repo"
  current_branch=$(git -C "$recorded_repo" branch --show-current 2>/dev/null || true)
  [[ -n $current_branch ]] || current_branch=detached-or-unknown
  [[ $current_branch == "$recorded_branch" ]] ||
    die "recorded branch '$recorded_branch' does not match current branch '$current_branch'"

  awk -v stage="$stage" '
    function pending(value, lowered) {
      lowered = tolower(value)
      return lowered == "" || lowered ~ /^pending([: -]|$)/
    }
    function save() {
      if (id != "") {
        if (!(id in seen)) {
          seen[id] = 1
          record_count++
        }
        disposition[id] = disp
        bhe[id] = bhe_validation
        bhce[id] = bhce_validation
        follow[id] = follow_up
        bhe_reference[id] = bhe_ref
        bhce_reference[id] = bhce_ref
      }
    }
    /^## / {
      save()
      id = disp = bhe_validation = bhce_validation = follow_up = bhe_ref = bhce_ref = ""
      next
    }
    /^- Change ID: / { id = substr($0, 14); next }
    /^- Disposition: / { disp = substr($0, 16); next }
    /^- BHE validation: / { bhe_validation = substr($0, 19); next }
    /^- BHCE validation: / { bhce_validation = substr($0, 20); next }
    /^- Follow-up: / { follow_up = substr($0, 14); next }
    /^- BHE reference: / { bhe_ref = substr($0, 18); next }
    /^- BHCE reference: / { bhce_ref = substr($0, 19); next }
    END {
      save()
      if (record_count == 0) {
        print "error: parity ledger has no change records" > "/dev/stderr"
        exit 1
      }
      failed = 0
      if (stage == "iteration") {
        exit 0
      }
      for (change in disposition) {
        if (disposition[change] == "investigate") {
          print "error: " change " still has disposition investigate" > "/dev/stderr"
          failed = 1
        }
        if (pending(bhe[change])) {
          print "error: " change " has pending BHE validation" > "/dev/stderr"
          failed = 1
        }
        if (pending(bhce[change])) {
          print "error: " change " has pending BHCE validation" > "/dev/stderr"
          failed = 1
        }
        if (disposition[change] == "deferred" &&
            (follow[change] == "" || follow[change] == "none" || pending(follow[change]))) {
          print "error: " change " is deferred without a concrete follow-up" > "/dev/stderr"
          failed = 1
        }
        if (pending(bhe_reference[change]) || bhe_reference[change] == "none") {
          print "error: " change " has no completed BHE reference" > "/dev/stderr"
          failed = 1
        }
        if ((disposition[change] == "matched" || disposition[change] == "equivalent") &&
            (pending(bhce_reference[change]) || bhce_reference[change] == "none")) {
          print "error: " change " requires a completed BHCE reference" > "/dev/stderr"
          failed = 1
        }
      }
      exit failed
    }
  ' "$entry_file"
  if [[ $stage == pr ]]; then
    printf 'Parity ledger is PR-ready: %s\n' "$entry_file"
  else
    printf 'Parity ledger is structurally valid for iteration: %s\n' "$entry_file"
  fi
  exit 0
fi

[[ $command_name == record ]] || die "unsupported command: $command_name"
validate_slug "--change-id" "$change_id"
[[ -n $change ]] || die "--change is required"
case "$surface" in
  regraph|sigma|shared-ui|api|backend|other) ;;
  *) die "--surface must be regraph, sigma, shared-ui, api, backend, or other" ;;
esac
case "$disposition" in
  matched|equivalent|bhe-only|intentionally-divergent|deferred|investigate) ;;
  *) die "invalid --disposition" ;;
esac
[[ -n $reason ]] || die "--reason is required"
[[ -n $bhe_validation ]] || die "--bhe-validation is required; use pending during iteration"
[[ -n $bhce_validation ]] || die "--bhce-validation is required; explain when testing is not required"
[[ -n $follow_up ]] || die "--follow-up is required; use none when no follow-up exists"
if [[ $disposition == deferred && ($follow_up == none || $follow_up == pending) ]]; then
  die "deferred changes require a concrete --follow-up"
fi

change=$(one_line "$change")
reason=$(one_line "$reason")
bhe_validation=$(one_line "$bhe_validation")
bhce_validation=$(one_line "$bhce_validation")
follow_up=$(one_line "$follow_up")
bhe_ref=$(one_line "$bhe_ref")
bhce_ref=$(one_line "$bhce_ref")
recorded_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

lock_dir=$entry_file.lock
mkdir "$lock_dir" 2>/dev/null || die "another process is updating $entry_file"
tmp_file=$(mktemp "${entry_file}.tmp.XXXXXX")
cleanup_record() {
  rm -f "$tmp_file"
  rmdir "$lock_dir" 2>/dev/null || true
}
trap cleanup_record EXIT

cp "$entry_file" "$tmp_file"
printf '\n## %s — %s\n\n- Change ID: %s\n- Change: %s\n- Surface: %s\n- Disposition: %s\n- Reason: %s\n- BHE validation: %s\n- BHCE validation: %s\n- Follow-up: %s\n- BHE reference: %s\n- BHCE reference: %s\n' \
  "$recorded_at" "$change_id" "$change_id" "$change" "$surface" "$disposition" "$reason" \
  "$bhe_validation" "$bhce_validation" "$follow_up" "$bhe_ref" "$bhce_ref" >> "$tmp_file"
mv "$tmp_file" "$entry_file"
chmod 600 "$entry_file"
rmdir "$lock_dir"
trap - EXIT
printf 'Recorded parity decision: %s (%s)\n' "$change_id" "$entry_file"
