---
name: timeline-markdown-notes
description: Extract timeline entries from Markdown operator notes.
icon: ./assets/icon.png
---

# Timeline Markdown Notes Parser

Use when Markdown or plain text notes are provided for timeline consolidation.

## Input Contract
- Directory `input/notes/` with `.md`/`.txt` files containing timestamped entries, log-style notes, lists, or tables.

## Output
- Write `output/md_notes_entries.json` with normalized entries (timestamp, source, operator, action, details, raw_timestamp).

## Workflow
1. Detect timestamp patterns (ISO 8601, MM/DD/YYYY, DD/MM/YYYY, HH:MM:SS) across text and list entries.
2. Use filename-derived date/operator context when time-only entries appear.
3. Normalize UTC timestamps and assign `operator` from filename patterns (`operator1-notes`, etc.).
4. Treat lists/tables as multi-entry sequences and map bullet text to `action`/`details`.
5. Flag ambiguous entries for manual review and record `raw_timestamp`.

## Notes
- Prefer strict patterns but allow friendly heuristics (headers like `## 2024-01-15 Morning Session`).
- Provide fallback steps for entries missing time but containing keywords such as `recon`, `auth`, `exploit`.
