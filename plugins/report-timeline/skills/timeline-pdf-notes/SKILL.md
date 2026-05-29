---
name: timeline-pdf-notes
description: Extract timeline entries from PDF operator notes via pdfplumber.
metadata:
  author: "GhostWorks"
---

# Timeline PDF Notes Parser

Use when provided operator notes are only available as PDFs.

## Input Contract
- Directory `input/notes/` with `.pdf` files representing operator notes.

## Output
- Write `output/pdf_notes_entries.json` with normalized entries (timestamp, source, operator, action, details, raw_timestamp).

## Workflow
1. Use `pdfplumber` to extract text per page and optional tables.
2. Apply the same timestamp patterns as the Markdown parser; use filename-derived dates/operator context when necessary.
3. Normalize timestamps to UTC and drop duplicates flagged by the consolidator.
4. Track page numbers or table origins in `source`/`details` for traceability.
5. Append `source_type = "pdf_notes"` in metadata with counts and errors.
6. Provide guidance to install `pdfplumber` if missing.

## Notes
- Tables are optional; parse them to capture structured timeline rows when available.
- Handle messy text by cleaning repeated headers/footers.
