#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bhe-isolated-stack.sh doctor
  bhe-isolated-stack.sh list [--json]
  bhe-isolated-stack.sh next-slot
  bhe-isolated-stack.sh <plan|up|seed|status|logs|down|archive> \
    --name NAME --slot N [--repo PATH] [options]

Commands:
  doctor     Check local prerequisites and report recorded-stack conflicts.
  list       Show recorded stacks, ownership, and runtime state.
  next-slot  Print the first unrecorded slot whose deterministic ports are free.
  plan       Generate, reserve, and validate configuration without starting.
  up         Start the stack and load missing official AD/Entra sample data.
  seed       Load missing official AD/Entra data into a running stack.
  status     Show only this stack's containers and connection details.
  logs       Show scoped stack logs; optionally pass --service SERVICE.
  down       Stop only this stack while preserving named volumes.
  archive    Archive generated state after all stack containers are removed.

Options:
  --accept-standard-eula  Permit standard EULA acceptance for local hosts only.
  --skip-sample-data      Start without sample data.
  --with-db-tools         Include PgAdmin and PgBadger for plan/up.
  --without-db-tools      Exclude PgAdmin and PgBadger for plan/up (default).
  --service SERVICE       Limit logs to one Compose service.
  --tail N                Number of log lines to show (default: 200).
  --json                  Emit machine-readable output for list.

Names must be unique task-specific lowercase slugs. Slots are 1-99 and are
globally reserved by plan until that stack's state is archived.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

have() {
  command -v "$1" >/dev/null 2>&1
}

command_name=${1:-}
case "$command_name" in
  doctor|list|next-slot|plan|up|seed|status|logs|down|archive) shift ;;
  -h|--help|'') usage; exit 0 ;;
  *) usage >&2; die "unknown command: $command_name" ;;
esac

name=
slot=
repo=
skip_sample_data=false
accept_standard_eula=false
db_tools_mode=preserve
json_output=false
service=
tail_lines=200

while (($#)); do
  case "$1" in
    --name) name=${2:-}; shift 2 ;;
    --slot) slot=${2:-}; shift 2 ;;
    --repo) repo=${2:-}; shift 2 ;;
    --skip-sample-data) skip_sample_data=true; shift ;;
    --accept-standard-eula) accept_standard_eula=true; shift ;;
    --with-db-tools) db_tools_mode=enabled; shift ;;
    --without-db-tools) db_tools_mode=disabled; shift ;;
    --service) service=${2:-}; shift 2 ;;
    --tail) tail_lines=${2:-}; shift 2 ;;
    --json) json_output=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

state_root=${BHE_ISOLATED_STATE_ROOT:-${XDG_STATE_HOME:-$HOME/.local/state}/codex-bhe-stacks}
base_repo=${BHE_BASE_REPO:-$HOME/Dev/bloodhound-enterprise}

manifest_files() {
  local manifest_file
  [[ -d $state_root ]] || return 0
  for manifest_file in "$state_root"/*/manifest.json; do
    [[ -f $manifest_file ]] && printf '%s\n' "$manifest_file"
  done | sort
}

runtime_state() {
  local manifest_file=$1
  local recorded_project recorded_repo
  recorded_project=$(jq -r '.project' "$manifest_file")
  recorded_repo=$(jq -r '.repo' "$manifest_file")

  if [[ ! -d $recorded_repo ]]; then
    printf 'stale-worktree'
  elif ! docker info >/dev/null 2>&1; then
    printf 'docker-unavailable'
  elif docker ps --filter "label=com.docker.compose.project=$recorded_project" \
    --format '{{.ID}}' | grep -q .; then
    printf 'running'
  elif docker ps -a --filter "label=com.docker.compose.project=$recorded_project" \
    --format '{{.ID}}' | grep -q .; then
    printf 'stopped-containers'
  else
    printf 'recorded'
  fi
}

emit_stack_json() {
  local manifest_file=$1
  local state updated
  state=$(runtime_state "$manifest_file")
  updated=$(stat -f '%Sm' "$manifest_file" 2>/dev/null ||
    stat -c '%y' "$manifest_file" 2>/dev/null || printf 'unknown')
  jq -c --arg state "$state" --arg updated "$updated" \
    '. + {state:$state, updated:$updated, manifest:input_filename}' "$manifest_file"
}

list_stacks() {
  local found=false manifest_file
  if $json_output; then
    while IFS= read -r manifest_file; do
      [[ -n $manifest_file ]] || continue
      emit_stack_json "$manifest_file"
    done < <(manifest_files) | jq -s '.'
    return
  fi

  while IFS= read -r manifest_file; do
    [[ -n $manifest_file ]] || continue
    found=true
    emit_stack_json "$manifest_file" |
      jq -r '"\(.name)\t\(.state)\t\(.project)\tslot=\(.slot)\t\(.url)\t\(.repo)\tupdated=\(.updated)"'
  done < <(manifest_files)
  $found || printf 'No recorded isolated BHE stacks under %s\n' "$state_root"
}

slot_ports_free() {
  local candidate=$1 port
  local ports=(
    $((18080 + candidate))
    $((18180 + candidate))
    $((18280 + candidate))
    $((18380 + candidate))
    $((18480 + candidate))
    $((18580 + candidate))
    $((18680 + candidate))
  )
  for port in "${ports[@]}"; do
    lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1 && return 1
  done
  return 0
}

slot_is_recorded() {
  local candidate=$1 manifest_file
  while IFS= read -r manifest_file; do
    [[ -n $manifest_file ]] || continue
    [[ $(jq -r '.slot' "$manifest_file") != "$candidate" ]] || return 0
  done < <(manifest_files)
  return 1
}

find_next_slot() {
  local candidate
  have jq || die "missing required command: jq"
  have lsof || die "missing required command: lsof"
  for candidate in $(seq 1 99); do
    if ! slot_is_recorded "$candidate" && slot_ports_free "$candidate"; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  die "no free isolated-stack slots from 1 to 99"
}

doctor() {
  local failed=false dependency worktree branch upstream manifest_file state
  for dependency in git just go node yarn docker jq sed curl lsof; do
    if have "$dependency"; then
      printf 'ok      %s\n' "$dependency"
    else
      printf 'missing %s\n' "$dependency"
      failed=true
    fi
  done

  if have docker && docker compose version >/dev/null 2>&1; then
    printf 'ok      docker-compose-v2\n'
  else
    printf 'missing docker-compose-v2\n'
    failed=true
  fi

  if have docker && docker info >/dev/null 2>&1; then
    printf 'ok      docker-daemon\n'
  else
    printf 'failed  docker-daemon\n'
    failed=true
  fi

  if [[ -d $base_repo ]]; then
    printf 'ok      base-clone\n'
    while IFS= read -r worktree; do
      [[ -n $worktree && -d $worktree ]] || continue
      branch=$(git -C "$worktree" branch --show-current 2>/dev/null || true)
      upstream=$(git -C "$worktree" rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || true)
      if [[ -n $branch && $branch != main && $upstream == origin/main ]]; then
        printf 'warning branch-upstream %s: %s -> origin/main\n' "$worktree" "$branch"
        failed=true
      fi
    done < <(git -C "$base_repo" \
      worktree list --porcelain | sed -n 's/^worktree //p')
  else
    printf 'missing base-clone %s\n' "$base_repo"
    failed=true
  fi

  if have jq; then
    collision_report=$(validate_recorded_manifests || true)
    if [[ -n $collision_report ]]; then
      printf '%s\n' "$collision_report"
      failed=true
    else
      printf 'ok      recorded-stack-ownership\n'
    fi
    while IFS= read -r manifest_file; do
      [[ -n $manifest_file ]] || continue
      state=$(runtime_state "$manifest_file")
      if [[ $state == stale-worktree ]]; then
        printf 'warning stale-stack %s\n' "$manifest_file"
        failed=true
      fi
    done < <(manifest_files)
  fi
  $failed && return 1
  return 0
}

validate_recorded_manifests() {
  local first second
  local manifests=()
  while IFS= read -r first; do
    [[ -n $first ]] && manifests+=("$first")
  done < <(manifest_files)

  local i j key first_value second_value failed=false
  for ((i = 0; i < ${#manifests[@]}; i++)); do
    first=${manifests[$i]}
    for ((j = i + 1; j < ${#manifests[@]}; j++)); do
      second=${manifests[$j]}
      for key in name project repo slot hostname; do
        first_value=$(jq -r --arg key "$key" '.[$key]' "$first")
        second_value=$(jq -r --arg key "$key" '.[$key]' "$second")
        if [[ $first_value == "$second_value" ]]; then
          printf 'collision %s=%s between %s and %s\n' \
            "$key" "$first_value" "$first" "$second"
          failed=true
        fi
      done
    done
  done
  $failed && return 1
  return 0
}

case "$command_name" in
  doctor) doctor; exit ;;
  list) list_stacks; exit ;;
  next-slot) find_next_slot; exit ;;
esac

[[ $name =~ ^[a-z0-9][a-z0-9-]{0,38}[a-z0-9]$ || $name =~ ^[a-z0-9]$ ]] ||
  die "--name must be a lowercase slug of 1-40 characters"
[[ $slot =~ ^[0-9]+$ ]] || die "--slot must be an integer from 1 to 99"
((slot >= 1 && slot <= 99)) || die "--slot must be from 1 to 99"
[[ $tail_lines =~ ^[0-9]+$ ]] || die "--tail must be a non-negative integer"
[[ -z $service || $command_name == logs ]] ||
  die "--service is valid only with logs"
$json_output && die "--json is valid only with list"
if $skip_sample_data && [[ $command_name != up ]]; then
  die "--skip-sample-data is valid only with up"
fi
if $accept_standard_eula && [[ $command_name != up && $command_name != seed ]]; then
  die "--accept-standard-eula is valid only with up or seed"
fi
if [[ $db_tools_mode != preserve && $command_name != plan && $command_name != up ]]; then
  die "--with-db-tools and --without-db-tools are valid only with plan or up"
fi

for dependency in docker git jq sed curl lsof; do
  have "$dependency" || die "missing required command: $dependency"
done
if [[ $command_name == seed || ($command_name == up && $skip_sample_data == false) ]]; then
  have node || die "missing required command: node"
fi
docker compose version >/dev/null || die "Docker Compose v2 is required"

if [[ -z $repo ]]; then
  repo=$(git rev-parse --show-toplevel 2>/dev/null) ||
    die "run inside a BHE worktree or pass --repo"
fi
repo=$(cd "$repo" && pwd -P)
[[ -f $repo/docker-compose.dev.yml && -f $repo/local-harnesses/build.config.json ]] ||
  die "not a BHE repository: $repo"

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
skill_dir=$(cd "$script_dir/.." && pwd -P)
template=$skill_dir/assets/docker-compose.isolated.yml.tmpl
traefik_template=$skill_dir/assets/traefik.isolated-dynamic.yml.tmpl
pruner_script=$skill_dir/scripts/prune-postgres-logs.sh
pgbadger_dockerfile=$skill_dir/assets/pgbadger.Dockerfile
[[ -f $template ]] || die "missing Compose override template: $template"
[[ -f $traefik_template ]] || die "missing Traefik template: $traefik_template"
[[ -f $pruner_script ]] || die "missing PostgreSQL log pruner: $pruner_script"
[[ -f $pgbadger_dockerfile ]] || die "missing PgBadger Dockerfile: $pgbadger_dockerfile"

project="bhe-isolated-$name"
state_dir=$state_root/$name
manifest=$state_dir/manifest.json
env_file=$state_dir/stack.env
override_file=$state_dir/docker-compose.isolated.yml
config_file=$state_dir/build.config.json
traefik_config_file=$state_dir/traefik.isolated-dynamic.yml

if [[ $db_tools_mode == preserve && -f $manifest ]]; then
  with_db_tools=$(jq -r '.db_tools // false' "$manifest")
elif [[ $db_tools_mode == enabled ]]; then
  with_db_tools=true
else
  with_db_tools=false
fi

web_port=$((18080 + slot))
traefik_port=$((18180 + slot))
api_port=$((18280 + slot))
toolapi_port=$((18380 + slot))
postgres_port=$((18480 + slot))
pgadmin_port=$((18580 + slot))
pgbadger_port=$((18680 + slot))

bhe_hostname="$name.bhe.localhost"
pgadmin_hostname="$name.pgadmin.localhost"
pgbadger_hostname="$name.pgbadger.localhost"
base_url="http://$bhe_hostname:$web_port"

compose() {
  local profiles=(--profile dev)
  $with_db_tools && profiles+=(--profile db-tools)
  COMPOSE_PROGRESS=${COMPOSE_PROGRESS:-plain} docker compose \
    --project-name "$project" \
    --env-file "$env_file" \
    -f "$repo/docker-compose.dev.yml" \
    -f "$override_file" \
    "${profiles[@]}" "$@"
}

assert_global_ownership() {
  local other other_name other_project other_repo other_slot other_hostname
  while IFS= read -r other; do
    [[ -n $other && $other != "$manifest" ]] || continue
    other_name=$(jq -r '.name' "$other")
    other_project=$(jq -r '.project' "$other")
    other_repo=$(jq -r '.repo' "$other")
    other_slot=$(jq -r '.slot' "$other")
    other_hostname=$(jq -r '.hostname' "$other")

    [[ $other_name != "$name" ]] ||
      die "stack name '$name' is owned by $other"
    [[ $other_project != "$project" ]] ||
      die "Compose project '$project' is owned by $other"
    [[ $other_repo != "$repo" ]] ||
      die "worktree '$repo' already owns stack '$other_name'; archive it or use its identity"
    [[ $other_slot != "$slot" ]] ||
      die "slot $slot is reserved by stack '$other_name'; choose another slot"
    [[ $other_hostname != "$bhe_hostname" ]] ||
      die "hostname '$bhe_hostname' is owned by stack '$other_name'"
  done < <(manifest_files)
}

verify_recorded_ownership() {
  [[ -f $manifest && -f $env_file && -f $override_file && -f $config_file ]] ||
    die "no complete recorded stack named '$name'"
  recorded_repo=$(jq -r '.repo' "$manifest")
  recorded_slot=$(jq -r '.slot' "$manifest")
  recorded_project=$(jq -r '.project' "$manifest")
  [[ $recorded_repo == "$repo" && $recorded_slot == "$slot" &&
    $recorded_project == "$project" ]] ||
    die "arguments do not match recorded ownership in $manifest"
}

sed_replacement() {
  printf '%s' "$1" | sed 's/[&|\\]/\\&/g'
}

write_stack_files() {
  mkdir -p "$state_dir"
  chmod 700 "$state_root" "$state_dir"
  assert_global_ownership

  if [[ -f $manifest ]]; then
    verify_recorded_ownership
  fi

  jq --arg root_url "$base_url/" \
    '.root_url = $root_url |
     .default_admin.email_address = "admin@example.com" |
     .default_admin.password = "ChangeMe123!" |
     .default_admin.expire_now = false' \
    "$repo/local-harnesses/build.config.json" > "$config_file.tmp"
  mv "$config_file.tmp" "$config_file"
  chmod 600 "$config_file"

  cat > "$env_file" <<EOF
WEB_PORT=127.0.0.1:$web_port
TRAEFIK_PORT=127.0.0.1:$traefik_port
BHE_API_PORT=127.0.0.1:$api_port
TOOLAPI_PORT=127.0.0.1:$toolapi_port
BHE_POSTGRES_PORT=127.0.0.1:$postgres_port
BHE_PG_ADMIN_PORT=127.0.0.1:$pgadmin_port
BHE_PGBADGER_PORT=127.0.0.1:$pgbadger_port
BHE_HOSTNAME=$bhe_hostname
BHE_PG_ADMIN_HOSTNAME=$pgadmin_hostname
VITE_HMR_CLIENT_PORT=$web_port
EOF
  chmod 600 "$env_file"

  escaped_config=$(sed_replacement "$config_file")
  escaped_traefik=$(sed_replacement "$traefik_config_file")
  escaped_skill_dir=$(sed_replacement "$skill_dir")
  escaped_pruner_script=$(sed_replacement "$pruner_script")
  sed \
    -e "s|__CONFIG_PATH__|$escaped_config|g" \
    -e "s|__TRAEFIK_CONFIG_PATH__|$escaped_traefik|g" \
    -e "s|__SKILL_DIR__|$escaped_skill_dir|g" \
    -e "s|__PRUNER_SCRIPT__|$escaped_pruner_script|g" \
    "$template" > "$override_file"

  sed \
    -e "s|__BHE_HOSTNAME__|$bhe_hostname|g" \
    -e "s|__PGADMIN_HOSTNAME__|$pgadmin_hostname|g" \
    -e "s|__PGBADGER_HOSTNAME__|$pgbadger_hostname|g" \
    "$traefik_template" > "$traefik_config_file"

  jq -n \
    --arg name "$name" \
    --arg project "$project" \
    --arg repo "$repo" \
    --argjson slot "$slot" \
    --arg url "$base_url/ui" \
    --arg hostname "$bhe_hostname" \
    --arg env_file "$env_file" \
    --arg override_file "$override_file" \
    --arg traefik_config_file "$traefik_config_file" \
    --argjson db_tools "$with_db_tools" \
    '{name:$name, project:$project, repo:$repo, slot:$slot, url:$url,
      hostname:$hostname, env_file:$env_file, override_file:$override_file,
      traefik_config_file:$traefik_config_file, db_tools:$db_tools}' > "$manifest.tmp"
  mv "$manifest.tmp" "$manifest"
  chmod 600 "$manifest"
}

show_connection() {
  username=$(jq -r '.default_admin.email_address // .default_admin.principal_name' "$config_file")
  password=$(jq -r '.default_admin.password' "$config_file")
  printf '\nStack:     %s\nWorktree:  %s\nURL:        %s/ui\nUsername:   %s\nPassword:   %s\nDB tools:   %s\nState:      %s\n' \
    "$project" "$repo" "$base_url" "$username" "$password" "$with_db_tools" "$state_dir"
}

seed_sample_data() {
  sample_script=${BHE_SAMPLE_DATA_SCRIPT:-$skill_dir/../bhe-sample-data-ingest/scripts/ingest_sample_data.cjs}
  [[ -f $sample_script ]] || die "sample-data ingest script not found: $sample_script"

  username=$(jq -r '.default_admin.email_address // .default_admin.principal_name' "$config_file")
  password=$(jq -r '.default_admin.password' "$config_file")
  login_payload=$(jq -nc --arg username "$username" --arg secret "$password" \
    '{login_method:"secret", username:$username, secret:$secret}')
  login_response=$(curl -fsS -X POST "$base_url/api/v2/login" \
    -H 'Content-Type: application/json' --data-binary "$login_payload") ||
    die "could not log in to $base_url to check sample data"
  token=$(printf '%s' "$login_response" | jq -r '.data.session_token // empty')
  [[ -n $token ]] || die "login succeeded without a session token"

  self_response=$(curl -fsS "$base_url/api/v2/self" -H "Authorization: Bearer $token")
  eula_accepted=$(printf '%s' "$self_response" | jq -r '.data.eula_accepted // false')
  if [[ $eula_accepted != true ]]; then
    $accept_standard_eula ||
      die "standard EULA is not accepted; rerun with --accept-standard-eula for this local stack"
    case "$bhe_hostname" in
      localhost|127.0.0.1|*.localhost)
        printf 'Accepting the standard EULA for isolated local development...\n'
        curl -fsS -X PUT "$base_url/api/v2/accept-eula" \
          -H "Authorization: Bearer $token" >/dev/null
        self_response=$(curl -fsS "$base_url/api/v2/self" -H "Authorization: Bearer $token")
        eula_accepted=$(printf '%s' "$self_response" | jq -r '.data.eula_accepted // false')
        [[ $eula_accepted == true ]] || die "local EULA acceptance did not persist"
        ;;
      *) die "refusing to accept a EULA automatically for non-local host: $bhe_hostname" ;;
    esac
  fi

  environments=$(curl -fsS "$base_url/api/v2/available-domains" -H "Authorization: Bearer $token")
  has_ad=$(printf '%s' "$environments" | jq 'any(.data[]?; .type == "active-directory")')
  has_entra=$(printf '%s' "$environments" | jq 'any(.data[]?; .type == "azure")')

  if [[ $has_ad == true && $has_entra == true ]]; then
    printf 'Official AD and Entra environments are present; skipping ingest.\n'
    return
  elif [[ $has_ad == false && $has_entra == false ]]; then
    dataset=both
  elif [[ $has_ad == false ]]; then
    dataset=ad
  else
    dataset=entra
  fi

  printf 'Loading missing official sample data (%s)...\n' "$dataset"
  node "$sample_script" \
    --base-url "$base_url" \
    --repo "$repo" \
    --username "$username" \
    --password "$password" \
    --dataset "$dataset" \
    --timeout-seconds 600
}

port_owner() {
  lsof -nP -iTCP:"$1" -sTCP:LISTEN 2>/dev/null |
    awk 'NR == 2 {print $1 " pid=" $2}' || true
}

assert_ports_available() {
  local port owner
  if docker ps --filter "label=com.docker.compose.project=$project" \
    --format '{{.ID}}' | grep -q .; then
    return
  fi
  for port in "$web_port" "$traefik_port" "$api_port" "$toolapi_port" \
    "$postgres_port" "$pgadmin_port" "$pgbadger_port"; do
    owner=$(port_owner "$port")
    [[ -z $owner ]] ||
      die "slot $slot port $port is already in use by $owner; choose another slot"
  done
}

case "$command_name" in
  plan)
    write_stack_files
    compose config --quiet
    printf 'Validated and reserved %s (slot %s). No containers were started.\n' \
      "$project" "$slot"
    show_connection
    ;;
  up)
    write_stack_files
    compose config --quiet
    assert_ports_available
    compose up -d --remove-orphans
    printf 'Waiting for the isolated API to become healthy...\n'
    healthy=false
    for _ in $(seq 1 60); do
      if curl -fsS "http://127.0.0.1:$api_port/health" >/dev/null 2>&1; then
        healthy=true
        break
      fi
      sleep 2
    done
    $healthy ||
      die "stack started but API did not become healthy within 120 seconds; inspect scoped logs"
    compose ps
    show_connection
    if [[ $skip_sample_data == false ]]; then
      seed_sample_data
    else
      printf 'Skipped sample-data ingest by request.\n'
    fi
    ;;
  seed)
    verify_recorded_ownership
    curl -fsS "http://127.0.0.1:$api_port/health" >/dev/null ||
      die "isolated API is not healthy; run up before seed"
    seed_sample_data
    ;;
  status)
    verify_recorded_ownership
    compose ps
    show_connection
    ;;
  logs)
    verify_recorded_ownership
    if [[ -n $service ]]; then
      compose logs --tail "$tail_lines" "$service"
    else
      compose logs --tail "$tail_lines"
    fi
    ;;
  down)
    verify_recorded_ownership
    compose down --remove-orphans
    printf 'Stopped %s. Named volumes and data were preserved.\n' "$project"
    ;;
  archive)
    verify_recorded_ownership
    docker info >/dev/null 2>&1 ||
      die "cannot verify stack state because the Docker daemon is unavailable"
    if docker ps -a --filter "label=com.docker.compose.project=$project" \
      --format '{{.ID}}' | grep -q .; then
      die "stack containers still exist; run down before archive"
    fi
    archive_root=$state_root/archive
    mkdir -p "$archive_root"
    chmod 700 "$archive_root"
    archived_at=$(date -u '+%Y%m%dT%H%M%SZ')
    archive_target=$archive_root/$name-$archived_at
    [[ ! -e $archive_target ]] || die "archive target already exists: $archive_target"
    mv "$state_dir" "$archive_target"
    printf 'Archived stack state to %s. Docker volumes were not deleted.\n' "$archive_target"
    ;;
esac
