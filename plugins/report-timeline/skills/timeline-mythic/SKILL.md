---
name: timeline-mythic
description: Parse Mythic export JSON into normalized timeline entries.
metadata:
  author: "GhostWorks"
---

# Timeline Mythic Parser

Trigger when Mythic exports (callbacks/tasks/responses/operations) are provided for timeline consolidation.

## Input Contract
- Directory `input/c2logs/mythic/` with JSON exports for callbacks, tasks, responses, or full operations.

## Output
- Produce `output/mythic_entries.json` with timeline entries (timestamp, source, operator, action, details, raw_timestamp).
- Add metadata with `source_type = "mythic"`, counts, and parse errors.

## Workflow
1. Detect export type (callbacks, tasks, full operations) by inspecting keys such as `callbacks`, `command_name`, or `timestamp`.
2. Convert all timestamps to ISO 8601 UTC (ensure `Z` suffix) using `fromisoformat` fallback patterns.
3. Emit entries:
   - Callback exports: `beacon_init` at `init_callback`, `checkin` at `last_checkin`.
   - Task exports: map `command_name`, `original_params`, or `display_params` to `action`/`details`.
   - Operation exports: iterate nested `callbacks` and `tasks`, keeping owner context.
4. Normalize `source` names to `Mythic-callback-<id>` or `Mythic-task-<id>`.
5. Include operator names, host/service details, and `action = task_name` with `details` from params/output.
6. Capture MITRE clues from command names when available (documented in the consolidator).

## Notes
- Favor `display_params` for human-readable commands.
- When `responses` arrays exist, include their output as part of the `details` field.
