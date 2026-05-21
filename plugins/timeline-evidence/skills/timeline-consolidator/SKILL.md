---
name: timeline-consolidator
description: Merge parsed timeline entries, apply MITRE tagging, and produce the final timeline outputs.
icon: ./assets/icon.png
---

# Timeline Consolidator

Use after parser skills to merge their JSON entries into the consolidated timeline.

## Input Contract
- JSON files in `output/`: `cs_entries.json`, `mythic_entries.json`, `terminal_entries.json`, `md_notes_entries.json`, `pdf_notes_entries.json`, `gw_entries.json`.

## Output
- `output/timeline.md` (markdown table) and `output/timeline.json` (normalized array) following the schema: timestamp, source, operator, action, details, mitre_tags, duplicate_flag, raw_timestamp.
- Metadata report summarizing counts per source, duplications, and MITRE tag coverage.

## Workflow
1. Load available entry files; skip missing ones but note their absence.
2. Normalize each entry:
   - Ensure timestamp is ISO 8601 UTC.
   - Guarantee `source`, `operator`, `action`, and `details` are filled.
3. Apply MITRE ATT&CK tagging using pattern mappings (discovery, execution, lateral movement, persistence, etc.) and add `mitre_tags` array.
4. Detect duplicates within a 5-second window per operator using textual similarity (SequenceMatcher). Flag duplicates with `duplicate_flag` and keep evidence of why flagged.
5. Merge entries, sort chronologically, and emit timeline table with columns (Timestamp, Source, Operator, MITRE, Action, Details).
6. Store diagnostics (parsers processed, duplicates found, errors) in metadata for reporting.
7. Preserve JSON-friendly `raw_timestamp` and `source_file` references for auditing.

## Notes
- Document MITRE pattern definitions in `references/mitre-patterns.md` for future tuning.
- Provide config knobs for duplicate detection window and similarity threshold (default 5s / 0.8 similarity).
