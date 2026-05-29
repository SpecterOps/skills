---
name: timeline-ghostwriter
description: Parse Ghostwriter oplog CSV exports into timeline entries.
metadata:
  author: "GhostWorks"
---

# Timeline Ghostwriter Parser

Trigger on Ghostwriter CSV oplog exports for timeline ingestion.

## Input Contract
- Directory `input/gw_oplog/` with `.csv` files exported from Ghostwriter operation logs.

## Output
- Write `output/gw_entries.json` with entries (timestamp, source, operator, action, details, command, output, source_ip, dest_ip, tool, user_context, raw_entry).
- Include metadata with `source_type = "ghostwriter"`, processing stats, and errors.

## Workflow
1. Discover CSV files and use `csv.Sniffer` to detect delimiters.
2. Validate required columns (`timestamp`, `operator`, `description`) before parsing.
3. Normalize Ghostwriter timestamps (support ISO 8601, US/EU formats) to `YYYY/MM/DD HH:MM:SS UTC`.
4. Map CSV columns to the standard schema, dedupe entries by `oplog_id`, and record the versioned `source_file`.
5. Capture context such as tool, command, source/dest IPs, and comments.
6. Write `metadata` including counts, files processed, and any CSV parsing issues.

## Notes
- Skip empty rows and rows missing both timestamp and description.
- Provide example timestamp formats and CSV validation warnings.
