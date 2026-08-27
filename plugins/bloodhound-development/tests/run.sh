#!/usr/bin/env bash
set -euo pipefail

plugin_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
environment_dir=$plugin_dir/skills/bhe-dev-environment
delivery_dir=$plugin_dir/skills/bhe-change-delivery
isolated=$environment_dir/scripts/bhe-isolated-stack.sh
parity=$delivery_dir/scripts/bhe-parity-log.sh
pr_context=$delivery_dir/scripts/check-pr-context.sh

test_root=$(mktemp -d "${TMPDIR:-/tmp}/bhe-development-tests.XXXXXX")
cleanup() {
  rm -rf "$test_root"
}
trap cleanup EXIT

pass_count=0
fail() {
  printf 'not ok - %s\n' "$*" >&2
  exit 1
}

pass() {
  pass_count=$((pass_count + 1))
  printf 'ok %s - %s\n' "$pass_count" "$1"
}

assert_contains() {
  local file=$1 expected=$2
  grep -F -- "$expected" "$file" >/dev/null ||
    fail "expected $file to contain: $expected"
}

assert_not_contains() {
  local file=$1 unexpected=$2
  if grep -F -- "$unexpected" "$file" >/dev/null; then
    fail "expected $file not to contain: $unexpected"
  fi
}

expect_failure() {
  local output_file=$1
  shift
  if "$@" >"$output_file" 2>&1; then
    fail "command unexpectedly succeeded: $*"
  fi
}

require_tools() {
  local tool
  for tool in git jq sed curl lsof; do
    command -v "$tool" >/dev/null 2>&1 || fail "missing test dependency: $tool"
  done
}

make_fake_commands() {
  local fake_bin=$1
  mkdir -p "$fake_bin"
  apply_fake_docker "$fake_bin/docker"
  apply_fake_gh "$fake_bin/gh"
  chmod +x "$fake_bin/docker" "$fake_bin/gh"
}

apply_fake_docker() {
  local target=$1
  sed 's/^+//' >"$target" <<'EOF'
+#!/usr/bin/env bash
+set -euo pipefail
+printf '%s\n' "$*" >>"${FAKE_DOCKER_LOG:?}"
+case "${1:-} ${2:-}" in
+  "compose version"|"info ") exit 0 ;;
+esac
+if [[ ${1:-} == ps ]]; then
+  exit 0
+fi
+if [[ ${1:-} == compose ]]; then
+  exit 0
+fi
+exit 0
EOF
}

apply_fake_gh() {
  local target=$1
  sed 's/^+//' >"$target" <<'EOF'
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ ${1:-} == repo && ${2:-} == view ]]; then
+  jq -n \
+    --arg name "${FAKE_GH_REPO:-SpecterOps/bloodhound-enterprise}" \
+    --arg visibility "${FAKE_GH_VISIBILITY:-PRIVATE}" \
+    --arg default_branch "${FAKE_GH_DEFAULT_BRANCH:-main}" \
+    '{nameWithOwner:$name, visibility:$visibility,
+      defaultBranchRef:{name:$default_branch}}'
+  exit 0
+fi
+printf 'unsupported fake gh invocation: %s\n' "$*" >&2
+exit 2
EOF
}

test_isolated_stack_guardrails() {
  local case_dir=$test_root/isolated fake_bin=$test_root/fake-bin
  local repo state docker_log output
  repo=$case_dir/repo
  state=$case_dir/state
  docker_log=$case_dir/docker.log
  output=$case_dir/output
  mkdir -p "$repo/local-harnesses" "$state"
  : >"$docker_log"
  printf 'services: {}\n' >"$repo/docker-compose.dev.yml"
  jq -n '{root_url:"http://bhe.localhost/", default_admin:{email_address:"old@example.com", password:"old", expire_now:true}}' \
    >"$repo/local-harnesses/build.config.json"

  FAKE_DOCKER_LOG=$docker_log PATH="$fake_bin:$PATH" BHE_ISOLATED_STATE_ROOT=$state \
    "$isolated" plan --name alpha --slot 1 --repo "$repo" >"$output"
  [[ -f $state/alpha/manifest.json ]] || fail "plan did not create a manifest"
  assert_contains "$docker_log" "config --quiet"
  assert_not_contains "$docker_log" "up -d"
  pass "isolated plan reserves ownership without starting containers"

  expect_failure "$output" env FAKE_DOCKER_LOG="$docker_log" PATH="$fake_bin:$PATH" \
    BHE_ISOLATED_STATE_ROOT="$state" "$isolated" plan --name beta --slot 2 --repo "$repo"
  assert_contains "$output" "already owns stack 'alpha'"
  pass "isolated plan rejects a second owner for the same worktree"

  expect_failure "$output" env FAKE_DOCKER_LOG="$docker_log" PATH="$fake_bin:$PATH" \
    BHE_ISOLATED_STATE_ROOT="$state" "$isolated" down --name alpha --slot 2 --repo "$repo"
  assert_contains "$output" "arguments do not match recorded ownership"
  pass "isolated down rejects an ownership tuple mismatch"

  : >"$docker_log"
  FAKE_DOCKER_LOG=$docker_log PATH="$fake_bin:$PATH" BHE_ISOLATED_STATE_ROOT=$state \
    "$isolated" down --name alpha --slot 1 --repo "$repo" >"$output"
  assert_contains "$docker_log" "down --remove-orphans"
  assert_not_contains "$docker_log" " -v"
  assert_not_contains "$docker_log" "--volumes"
  pass "isolated down preserves named volumes"

  expect_failure "$output" env FAKE_DOCKER_LOG="$docker_log" PATH="$fake_bin:$PATH" \
    BHE_ISOLATED_STATE_ROOT="$state" "$isolated" plan --name gamma --slot 3 \
    --repo "$repo" --accept-standard-eula
  assert_contains "$output" "--accept-standard-eula is valid only with up or seed"
  pass "isolated plan does not broaden EULA authorization"
}

test_parity_gate() {
  local case_dir=$test_root/parity repo state output
  repo=$case_dir/repo
  state=$case_dir/state
  output=$case_dir/output
  mkdir -p "$repo"
  git -C "$repo" init -q -b feature
  git -C "$repo" config user.name Test
  git -C "$repo" config user.email test@example.com
  printf 'fixture\n' >"$repo/fixture.txt"
  git -C "$repo" add fixture.txt
  git -C "$repo" -c commit.gpgsign=false commit -qm fixture

  BHE_PARITY_STATE_ROOT=$state "$parity" init --task delivery --repo "$repo" >"$output"
  BHE_PARITY_STATE_ROOT=$state "$parity" record \
    --task delivery --change-id behavior --change "Change behavior" --surface api \
    --disposition investigate --reason "Pending contract review" \
    --bhe-validation pending --bhce-validation pending --follow-up pending >"$output"
  BHE_PARITY_STATE_ROOT=$state "$parity" check --task delivery --stage iteration >"$output"
  expect_failure "$output" env BHE_PARITY_STATE_ROOT="$state" \
    "$parity" check --task delivery --stage pr
  assert_contains "$output" "still has disposition investigate"
  pass "parity iteration accepts work in progress while PR gate rejects it"

  BHE_PARITY_STATE_ROOT=$state "$parity" record \
    --task delivery --change-id behavior --change "Change behavior" --surface api \
    --disposition matched --reason "Both products share the contract" \
    --bhe-validation "go test ./... passed" --bhce-validation "go test ./... passed" \
    --follow-up none --bhe-ref abc123 --bhce-ref def456 >"$output"
  BHE_PARITY_STATE_ROOT=$state "$parity" check --task delivery --stage pr >"$output"
  assert_contains "$output" "Parity ledger is PR-ready"
  pass "parity PR gate accepts a completed matched disposition"

  git -C "$repo" checkout -qb other
  expect_failure "$output" env BHE_PARITY_STATE_ROOT="$state" \
    "$parity" check --task delivery --stage pr
  assert_contains "$output" "does not match current branch"
  pass "parity gate rejects a ledger from another branch"
}

test_pr_context() {
  local case_dir=$test_root/pr-context repo bare output
  local fake_bin=$test_root/fake-bin
  repo=$case_dir/repo
  bare=$case_dir/origin.git
  output=$case_dir/output
  mkdir -p "$repo"
  git init -q --bare "$bare"
  git -C "$repo" init -q -b main
  git -C "$repo" config user.name Test
  git -C "$repo" config user.email test@example.com
  printf 'fixture\n' >"$repo/fixture.txt"
  git -C "$repo" add fixture.txt
  git -C "$repo" -c commit.gpgsign=false commit -qm fixture
  git -C "$repo" remote add origin "$bare"
  git -C "$repo" checkout -qb feature
  git -C "$repo" push -qu origin feature

  (cd "$repo" && PATH="$fake_bin:$PATH" FAKE_GH_VISIBILITY=PUBLIC "$pr_context") >"$output"
  [[ $(jq -r '.visibility' "$output") == PUBLIC ]] || fail "visibility mismatch"
  [[ $(jq -r '.already_pushed' "$output") == true ]] || fail "push-state mismatch"
  [[ $(jq -r '.working_tree_clean' "$output") == true ]] || fail "clean-state mismatch"
  pass "PR preflight resolves visibility, branch, and pushed state"

  printf 'ahead\n' >>"$repo/fixture.txt"
  git -C "$repo" add fixture.txt
  git -C "$repo" -c commit.gpgsign=false commit -qm ahead
  (cd "$repo" && PATH="$fake_bin:$PATH" FAKE_GH_VISIBILITY=PRIVATE "$pr_context") >"$output"
  [[ $(jq -r '.already_pushed' "$output") == false ]] ||
    fail "ahead-of-upstream branch reported as pushed"
  [[ $(jq -r '.working_tree_clean' "$output") == true ]] || fail "ahead branch should be clean"
  pass "PR preflight rejects a clean branch with unpushed commits"

  git -C "$repo" checkout -qb local-only
  printf 'dirty\n' >>"$repo/fixture.txt"
  (cd "$repo" && PATH="$fake_bin:$PATH" FAKE_GH_VISIBILITY=PRIVATE "$pr_context") >"$output"
  [[ $(jq -r '.already_pushed' "$output") == false ]] || fail "unpushed branch mismatch"
  [[ $(jq -r '.working_tree_clean' "$output") == false ]] || fail "dirty-state mismatch"
  pass "PR preflight distinguishes unpushed and dirty work"
}

test_eval_schemas() {
  local skill eval_file
  for skill in bhe-dev-bootstrap bhe-dev-environment bhe-change-delivery bhe-enterprise-review bhe-ui-playwright bhe-sample-data-ingest; do
    eval_file=$plugin_dir/skills/$skill/evals/evals.json
    jq -e --arg skill "$skill" '
      .skill_name == $skill and
      (.evals | length) >= 3 and
      ([.evals[].id] | length == (unique | length)) and
      all(.evals[];
        (.id | type) == "number" and
        (.prompt | type) == "string" and length > 0 and
        (.expected_output | type) == "string" and length > 0 and
        (.files | type) == "array" and
        (.expectations | type) == "array" and length > 0)
    ' "$eval_file" >/dev/null || fail "invalid eval schema: $eval_file"
  done
  pass "BHE workflow skills ship canonical behavioral eval definitions"
}

require_tools
make_fake_commands "$test_root/fake-bin"
test_isolated_stack_guardrails
test_parity_gate
test_pr_context
test_eval_schemas
printf '1..%s\n' "$pass_count"
