#!/bin/sh
set -eu

log_directory=${POSTGRES_LOG_DIRECTORY:-/logs}
retention_count=${POSTGRES_LOG_RETENTION_COUNT:-8}
interval_seconds=${POSTGRES_LOG_PRUNE_INTERVAL_SECONDS:-300}
prune_once=${POSTGRES_LOG_PRUNE_ONCE:-false}

case "$retention_count" in
  ''|*[!0-9]*|0) echo "POSTGRES_LOG_RETENTION_COUNT must be a positive integer" >&2; exit 2 ;;
esac
case "$interval_seconds" in
  ''|*[!0-9]*|0) echo "POSTGRES_LOG_PRUNE_INTERVAL_SECONDS must be a positive integer" >&2; exit 2 ;;
esac
case "$prune_once" in
  true|false) ;;
  *) echo "POSTGRES_LOG_PRUNE_ONCE must be true or false" >&2; exit 2 ;;
esac

prune_logs() {
  [ -d "$log_directory" ] || return 0
  log_count=$(find "$log_directory" -maxdepth 1 -type f -name 'postgresql-*.log' | wc -l | tr -d ' ')
  remove_count=$((log_count - retention_count))
  [ "$remove_count" -gt 0 ] || return 0
  find "$log_directory" -maxdepth 1 -type f -name 'postgresql-*.log' -print0 |
    xargs -0 ls -1tr |
    sed -n "1,${remove_count}p" |
    while IFS= read -r log_file; do
      rm -f -- "$log_file"
    done
}

while :; do
  prune_logs
  [ "$prune_once" = true ] && exit 0
  sleep "$interval_seconds"
done
