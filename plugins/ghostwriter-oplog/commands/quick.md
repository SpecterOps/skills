---
description: Quick timestamped oplog entry for key events
allowed-tools:
  - Bash
  - mcp__ghostwriter__create_oplog_entry
argument-hint: "<description> [--tags tag1,tag2]"
---

Log a timestamped entry to the GhostWriter oplog.

## Steps

1. Get settings from environment variables:
   - `GW_OPLOG_ID` (required)
   - `GW_OPERATOR_NAME` (required)
   - `GW_SOURCE_IP` (optional)

2. If required env vars missing, tell user to run `/ghostwriter-oplog:config` and stop.

3. Parse arguments:
   - Everything before `--tags` is the description
   - `--tags` value is comma-separated list of tags

4. Get current timestamp by running: `date -u +"%Y-%m-%dT%H:%M:%SZ"`

5. Call `create_oplog_entry` with:
   - `oplog_id`: from GW_OPLOG_ID
   - `operator_name`: from GW_OPERATOR_NAME
   - `source_ip`: from GW_SOURCE_IP (if set)
   - `description`: from user argument
   - `start_date`: timestamp from step 4
   - `tags`: from --tags argument (if provided)

6. Confirm entry was logged with the entry ID.
