#!/usr/bin/env bash
set -euo pipefail

refresh_seconds=${PGBADGER_REFRESH_SECONDS:-900}
retention_days=${PGBADGER_REPORT_RETENTION_DAYS:-2}

[[ $refresh_seconds =~ ^[1-9][0-9]*$ ]] ||
  { echo "PGBADGER_REFRESH_SECONDS must be a positive integer" >&2; exit 2; }
[[ $retention_days =~ ^[1-9][0-9]*$ ]] ||
  { echo "PGBADGER_REPORT_RETENTION_DAYS must be a positive integer" >&2; exit 2; }

mkdir -p /app/reports
shopt -s nullglob

while true; do
  logs=(/app/logs/postgresql-*.log)
  if (("${#logs[@]}" > 0)); then
    pgbadger --format stderr --prefix '%m [%p] %q%u@%d ' --incremental --quiet \
      --retention "${retention_days}" --outdir /app/reports "${logs[@]}"
  fi
  sleep "$refresh_seconds"
done
