---
name: timeline-cobaltstrike
description: Parse Cobalt Strike logs into normalized timeline entries for the reporting workflow.
metadata:
  author: "GhostWorks"
---

# Timeline Cobalt Strike Parser

Use this skill when the task mentions Cobalt Strike logs, beacon sessions, or the need to capture CS operator commands for the consolidated timeline.

## Input Contract
- Expect a directory (`input/c2logs/cobaltstrike/`) containing beacon logs, `weblog.log`, `events.log`, and optional keystroke captures.
- Support standard filenames such as `beacon_<id>.log`, `weblog.log`, `events.log`, and `keystrokes_<id>.txt`.

## Output
- Write JSON to `output/cs_entries.json` with entries that share the timeline schema (timestamp, source, operator, action, details, raw_timestamp).
- Include metadata such as files processed, entries count, and any parsing errors.

## Workflow
1. Normalize timestamps from the CS format (`MM/DD YYYY HH:MM:SS UTC`) to ISO 8601 UTC.
2. Split each log block by timestamps and detect tags (`[metadata]`, `[input]`, `[output]`, `[task]`, `[checkin]`).
3. Extract operator, command, and command outputs; map `[input]` lines to action/command details.
4. Capture Web and Event log lines as summary entries (`web_hit`, `joined`, `hosted`, etc.).
5. If keystroke files lack timestamps, annotate entries using file mtime and the filename-derived context.
6. Emit every entry with `source` (`CS-beacon-<id>` or similar) and `raw_timestamp` for traceability.
7. Write `metadata.source_type = "cobaltstrike"` plus counters and any errors.

## Notes
- Treat `[metadata]` entries as `beacon_init` with details about host, user, and IP.
- Use the filename to derive the beacon ID for the `source` field.
- When `[output]` follows `[input]`, attach the output to the preceding command entry.
