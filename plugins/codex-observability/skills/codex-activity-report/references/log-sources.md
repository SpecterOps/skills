# Codex Activity Report Sources

Use this reference only when you need to understand source precedence or explain why a report includes a specific event.

## Source Order

1. `rollout`:
   Live rollout JSONL files and archived rollout JSONL files in `.codex/sessions/`.
   These contain the richest chronology: session metadata, user prompts, assistant messages, reasoning summaries, tool calls, tool outputs, task lifecycle messages, and web-search activity.
2. `tui_log`:
   `.codex/log/codex-tui.log`.
   Use this to capture active-session tool calls, warnings, and shutdown messages that may not have landed in a rollout file yet.
3. `history`:
   `.codex/history.jsonl`.
   Use this as a fallback for exact user prompt text and session ids when rollout data is missing.
4. `sqlite`:
   `.codex/logs*.sqlite`.
   Use this to recover warnings, errors, shutdowns, and tool-call traces that overlap with or supplement the TUI log.
5. `state`:
   `.codex/state/**`.
   Use this for planner tasks, evidence indexes, and agent-result artifacts. These files usually lack embedded timestamps, so the report relies on filesystem modification time and must say so.

## Normalization Rules

- Keep prompts, approvals, patches, warnings, errors, and saved state artifacts discrete.
- Collapse repetitive read-only inspection commands into a single batch event.
- Collapse repeated empty `write_stdin` polls into a single PTY-poll event.
- Merge tool calls with their tool outputs when a shared `call_id` exists.
- Treat `compacted` and `context_compacted` records as metadata only so the report does not double-count older conversation history.
- When `--focus-pattern` is supplied, seed sessions from matching events and then keep all events from those sessions so the report stays coherent.

## Narrative Style

- Keep the narrative in active voice.
- Use `the operator`, `Codex`, or `the Codex harness` for actor names.
- Quote user prompts and exact commands verbatim when available.
- Keep all timestamps in UTC.
- For the first sentence of a day, use `On <Month Day, Year> at HH:MM:SS UTC, ...`.
- For later sentences on the same day, use `At HH:MM:SS UTC, ...`.
