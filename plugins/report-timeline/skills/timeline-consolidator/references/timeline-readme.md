# Timeline Workflow Reference

Use this reference to understand how the timeline pipeline consumes inputs and produces outputs.

- Parsers expect input directories:
  - `input/c2logs/cobaltstrike/`
  - `input/c2logs/mythic/`
  - `input/terminallogs/`
  - `input/notes/` (Markdown/PDF)
  - `input/gw_oplog/`
- Parser outputs are JSON files under `output/` that follow a shared schema.
- `timeline-consolidator` merges those JSON files, adds MITRE tags, handles duplicates, and writes `timeline.md` and `timeline.json`.
- `timeline-workflow` runs the parsers first then the consolidator; missing inputs are documented in `timeline-gaps.txt`.

Refer to `references/timeline-config.yaml` for tuning timezone/duplicate/mitre defaults and `references/mitre-patterns.md` for the regex rules.
