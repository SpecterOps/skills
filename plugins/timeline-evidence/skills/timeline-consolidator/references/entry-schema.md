# Timeline Entry Schema

Each parser writes entries that the consolidator merges. Ensure the following fields appear in every JSON entry:

- `timestamp` (ISO 8601 UTC string)
- `source` (e.g., CS-beacon-12345, Mythic-task-100, terminal-session)
- `operator` (operator username or system for automated events)
- `action` (short verb describing the event)
- `details` (free-text details, e.g., full command or log line)
- `raw_timestamp` (original timestamp string from the source)
- `mitre_tags` (array added by the consolidator)
- `duplicate_flag` (boolean set by the consolidator)
- Additional source-specific metadata such as `command`, `output`, `source_ip`, `dest_ip`, `tool`, `user_context`, and `source_file` may also be present for auditing.
