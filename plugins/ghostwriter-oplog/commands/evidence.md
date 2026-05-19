---
description: Log oplog entry with file contents as evidence
allowed-tools:
  - Bash
  - Read
  - mcp__ghostwriter__create_oplog_entry
argument-hint: "<file-path> <description> [--tags tag1,tag2]"
---

Log a timestamped entry to the GhostWriter oplog with file contents as evidence.

## Steps

1. Get settings from environment variables:
   - `GW_OPLOG_ID` (required)
   - `GW_OPERATOR_NAME` (required)
   - `GW_SOURCE_IP` (optional)

2. If required env vars missing, tell user to run `/ghostwriter-oplog:config` and stop.

3. Parse arguments:
   - First argument is the file path
   - Remaining text before `--tags` is the description
   - `--tags` value is comma-separated list of tags

4. Read the evidence file:
   - If file doesn't exist, report error and stop
   - If file is binary (image, etc.), note the file path in output instead of contents

5. Get current timestamp by running: `date -u +"%Y-%m-%dT%H:%M:%SZ"`

6. Call `create_oplog_entry` with:
   - `oplog_id`: from GW_OPLOG_ID
   - `operator_name`: from GW_OPERATOR_NAME
   - `source_ip`: from GW_SOURCE_IP (if set)
   - `description`: include file path in description, e.g., "Evidence: /path/to/file - user's description"
   - `output`: file contents (or "[Binary file: /path/to/file]" for non-text)
   - `start_date`: timestamp from step 5
   - `tags`: from --tags argument (if provided)

7. Confirm entry was logged with the entry ID and note the file path was included.
