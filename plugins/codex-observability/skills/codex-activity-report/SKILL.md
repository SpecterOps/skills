---
name: codex-activity-report
description: Generate a normalized UTC timeline and evidence-based narrative from Codex activity artifacts. Use when Codex needs to turn `.codex` logs, rollout JSONL files, archived session bundles, history files, SQLite logs, or planner state into Markdown reporting under `reports/`, especially for after-action reporting, operator handoff, chronology reconstruction, or evidence-backed engagement summaries.
---

# Codex Activity Report

## Overview

Generate two Markdown reports from the local Codex evidence trail: a normalized timeline and a narrative chronology. Use the bundled generator to preserve exact UTC timestamps, exact operator prompts, and exact command strings while keeping the output readable.

## Workflow

1. Resolve the target repository root. Default to the current repository when it contains `.codex/`.
2. Run the bundled generator script and let it write into `reports/`.
3. Review the generated Markdown only for obvious formatting issues or user-requested voice changes. Do not rewrite timestamps, prompts, or commands.
4. Keep both outputs in UTC.

## Command

Run the generator from the repository root or pass `--repo-root` explicitly:

```bash
python3 plugins/codex-observability/skills/codex-activity-report/scripts/generate_codex_activity_report.py
```

Useful flags:

- `--repo-root /absolute/path/to/repo`
- `--codex-home /absolute/path/to/.codex`
- `--output-dir /absolute/path/to/repo/reports`
- `--timeline-name custom-timeline.md`
- `--narrative-name custom-narrative.md`
- `--session-id <session-id>`
- `--focus-pattern 'app-server-experiments|codex-app-server-client'`
- `--no-archives`

Use `--focus-pattern` when you want a report for one workstream inside a larger `.codex` history. The generator seeds sessions from matching events and then keeps the full session chronology so the resulting timeline does not lose nearby actions that used generic commands.

## Output Rules

- Write the reports to `reports/` unless the operator asks for a different output directory.
- Generate a normalized timeline:
  - keep prompts, approvals, patches, warnings, errors, and saved state artifacts discrete;
  - group repetitive read-only inspection commands and empty PTY polls.
- Generate a narrative chronology:
  - keep the tone evidence-based and in active voice;
  - use `the operator`, `Codex`, or `the Codex harness` as the actor names;
  - use `On <Month Day, Year> at HH:MM:SS UTC, ...` for the first event of a day;
  - use `At HH:MM:SS UTC, ...` for later same-day events.
- Quote user prompts and exact commands verbatim when the artifacts contain them.
- Preserve UTC in both files even when the source artifact also exposes local filesystem metadata.

## Sources

The generator already knows how to parse the primary Codex artifacts in this repository class:

- rollout JSONL files under `.codex/sessions/`
- archived rollout JSONL files inside `.codex/sessions/**/*.zip`
- `.codex/history.jsonl`
- `.codex/log/codex-tui.log`
- `.codex/logs*.sqlite`
- planner and agent artifacts under `.codex/state/`

Read `references/log-sources.md` only when you need the exact precedence and normalization details.
