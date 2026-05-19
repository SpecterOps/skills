#!/usr/bin/env python3
"""Generate normalized Codex activity reports from local .codex artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sqlite3
import sys
import zipfile
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


SOURCE_RANKS = {
    "rollout": 50,
    "tui_log": 40,
    "history": 30,
    "sqlite": 20,
    "state": 10,
}

UTC = timezone.utc

READ_ONLY_COMMANDS = {
    "awk",
    "basename",
    "cat",
    "cut",
    "date",
    "dirname",
    "du",
    "echo",
    "env",
    "file",
    "find",
    "grep",
    "head",
    "ls",
    "lsof",
    "md5",
    "md5sum",
    "nl",
    "pbcopy",
    "pbpaste",
    "printf",
    "ps",
    "pwd",
    "realpath",
    "rg",
    "sed",
    "shasum",
    "sort",
    "sqlite3",
    "stat",
    "tail",
    "type",
    "uniq",
    "unzip",
    "wc",
    "which",
}

TIMESTAMP_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)\s+"
    r"(?P<level>[A-Z]+)\s+(?P<rest>.*)$"
)
THREAD_ID_RE = re.compile(r"thread_id=([0-9a-fA-F-]{8,})")
ROLLOUT_SESSION_RE = re.compile(r"rollout-[^-]+-[^-]+-[^-]+-(?P<sid>[0-9a-fA-F-]{8,})\.jsonl$")
PATCH_FILE_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.MULTILINE)
PATCH_MOVE_RE = re.compile(r"^\*\*\* Move to: (.+)$", re.MULTILINE)
EXIT_CODE_RE = re.compile(r"(?:Exit code:|EXIT:)\s*(\d+)")
COMMAND_WRITE_RE = re.compile(
    r"(^|[;&|]\s*)(?:mkdir|mv|cp|chmod|chown|touch|tee|rm|git\s+apply|git\s+clone|"
    r"docker(?:-compose)?\s+(?:compose\s+)?(?:up|down|restart)|python(?:3)?\s+.+\s+-m\s+pip)"
)
BOOTSTRAP_PROMPT_RE = re.compile(
    r"^(# AGENTS\.md instructions|<environment_context>|<skill>|<INSTRUCTIONS>)"
)


@dataclass(order=True)
class Event:
    sort_key: tuple = field(init=False, repr=False)
    timestamp: datetime
    kind: str
    title: str
    actor: str
    summary: str
    source: str
    source_type: str
    source_rank: int
    session_id: str | None = None
    call_id: str | None = None
    tool_name: str | None = None
    command: str | None = None
    quote: str | None = None
    output: str | None = None
    level: str | None = None
    status: str | None = None
    path_list: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.sort_key = (
            self.timestamp,
            self.session_id or "",
            self.kind,
            self.title,
            self.source,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a normalized Codex timeline and narrative."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root that contains .codex and will receive reports/.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        help="Override the Codex home directory. Defaults to <repo-root>/.codex.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for generated Markdown. Defaults to <repo-root>/reports.",
    )
    parser.add_argument(
        "--timeline-name",
        default="codex-timeline.md",
        help="Timeline output filename.",
    )
    parser.add_argument(
        "--narrative-name",
        default="codex-narrative.md",
        help="Narrative output filename.",
    )
    parser.add_argument(
        "--session-id",
        help="Limit reporting to a single session id when present.",
    )
    parser.add_argument(
        "--focus-pattern",
        action="append",
        default=[],
        help=(
            "Seed matching sessions from a regex pattern and then keep all events from those sessions. "
            "Repeat this flag for multiple patterns."
        ),
    )
    parser.add_argument(
        "--no-archives",
        action="store_true",
        help="Skip archived rollout JSONL files stored in zip files.",
    )
    return parser.parse_args()


def parse_iso_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def format_timestamp(dt: datetime) -> str:
    dt = dt.astimezone(UTC)
    base = dt.strftime("%Y-%m-%d %H:%M:%S")
    if dt.microsecond:
        millisecond = dt.microsecond // 1000
        if millisecond:
            return f"{base}.{millisecond:03d} UTC"
        return f"{base}.{dt.microsecond:06d} UTC"
    return f"{base} UTC"


def narrative_prefix(dt: datetime, include_day: bool) -> str:
    dt = dt.astimezone(UTC)
    time_text = format_timestamp(dt).replace(dt.strftime("%Y-%m-%d "), "")
    if include_day:
        return f"On {dt.strftime('%B')} {dt.day}, {dt.year} at {time_text}"
    return f"At {time_text}"


def normalize_ws(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def shorten(value: str | None, limit: int = 220) -> str:
    text = normalize_ws(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def parse_json_maybe(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
            continue
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
            continue
        for key in ("input_text", "output_text"):
            if isinstance(item.get(key), str):
                parts.append(item[key])
    return "\n".join(part for part in parts if part)


def extract_reasoning_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary")
    if isinstance(summary, list):
        parts: list[str] = []
        for item in summary:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
                    continue
                if item.get("type") == "summary_text" and isinstance(item.get("text"), str):
                    parts.append(item["text"])
        if parts:
            return "\n".join(parts)
    text = payload.get("text")
    if isinstance(text, str):
        return text
    return ""


def extract_command(args: Any) -> str | None:
    if isinstance(args, dict):
        for key in ("cmd", "command"):
            value = args.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        if args.get("tool_uses") and isinstance(args["tool_uses"], list):
            rendered: list[str] = []
            for tool_use in args["tool_uses"]:
                if not isinstance(tool_use, dict):
                    continue
                recipient = tool_use.get("recipient_name")
                parameters = tool_use.get("parameters")
                if isinstance(parameters, dict):
                    command = extract_command(parameters)
                    if command:
                        rendered.append(f"{recipient}: {command}")
                    else:
                        rendered.append(f"{recipient}: {json.dumps(parameters, sort_keys=True)}")
                else:
                    rendered.append(str(recipient))
            if rendered:
                return "\n".join(rendered)
    return None


def extract_patch_paths(text: str | None) -> list[str]:
    if not text:
        return []
    paths = PATCH_FILE_RE.findall(text)
    paths.extend(PATCH_MOVE_RE.findall(text))
    deduped: list[str] = []
    seen: set[str] = set()
    for path in paths:
        cleaned = path.strip()
        if cleaned and cleaned not in seen:
            deduped.append(cleaned)
            seen.add(cleaned)
    return deduped


def parse_tool_output(raw: str | None) -> tuple[str | None, str | None, list[str]]:
    if not raw:
        return None, None, []
    parsed = parse_json_maybe(raw)
    text = raw.strip()
    if isinstance(parsed, dict):
        nested_output = parsed.get("output")
        if isinstance(nested_output, str):
            text = nested_output.strip()
        metadata = parsed.get("metadata")
        if isinstance(metadata, dict) and metadata.get("exit_code") is not None:
            return str(metadata["exit_code"]), text, extract_patch_paths(text)
    exit_match = EXIT_CODE_RE.search(text)
    exit_code = exit_match.group(1) if exit_match else None
    return exit_code, text, extract_patch_paths(text)


def event_signature(event: Event) -> tuple[str, str, str, str, str]:
    timestamp_precision = "milliseconds"
    if event.kind in {
        "assistant_message",
        "reasoning",
        "session_context",
        "task_complete",
        "task_started",
        "tool_call",
        "tool_execution",
        "user_prompt",
        "warning",
        "web_lookup",
    }:
        timestamp_precision = "seconds"
    timestamp_key = event.timestamp.astimezone(UTC).isoformat(timespec=timestamp_precision)
    if event.quote:
        text_key = normalize_ws(event.quote)
    elif event.command:
        text_key = normalize_ws(event.command)
    elif event.output:
        text_key = normalize_ws(event.output[:300])
    else:
        text_key = normalize_ws(event.summary)
    return (
        timestamp_key,
        event.session_id or "",
        event.kind,
        event.tool_name or "",
        text_key,
    )


def event_richness(event: Event) -> int:
    return sum(
        len(part or "")
        for part in (event.summary, event.quote, event.command, event.output)
    ) + len(event.path_list) * 10


def should_keep_better(existing: Event, candidate: Event) -> bool:
    if candidate.source_rank != existing.source_rank:
        return candidate.source_rank > existing.source_rank
    return event_richness(candidate) > event_richness(existing)


def derive_rollout_session_id(name: str) -> str | None:
    match = ROLLOUT_SESSION_RE.search(name)
    if match:
        return match.group("sid")
    return None


def is_bootstrap_prompt(text: str | None) -> bool:
    if not text:
        return False
    return bool(BOOTSTRAP_PROMPT_RE.match(text.strip()))


def create_event(
    *,
    timestamp: datetime,
    kind: str,
    title: str,
    actor: str,
    summary: str,
    source: str,
    source_type: str,
    session_id: str | None = None,
    call_id: str | None = None,
    tool_name: str | None = None,
    command: str | None = None,
    quote: str | None = None,
    output: str | None = None,
    level: str | None = None,
    status: str | None = None,
    path_list: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> Event:
    return Event(
        timestamp=timestamp,
        kind=kind,
        title=title,
        actor=actor,
        summary=summary,
        source=source,
        source_type=source_type,
        source_rank=SOURCE_RANKS[source_type],
        session_id=session_id,
        call_id=call_id,
        tool_name=tool_name,
        command=command,
        quote=quote,
        output=output,
        level=level,
        status=status,
        path_list=path_list or [],
        metadata=metadata or {},
    )


def parse_rollout_events(
    lines: Iterable[str],
    source_label: str,
    file_hint: str,
    stats: Counter,
) -> list[Event]:
    events: list[Event] = []
    session_id = derive_rollout_session_id(file_hint)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            stats["rollout_decode_errors"] += 1
            continue
        timestamp_raw = record.get("timestamp")
        if not isinstance(timestamp_raw, str):
            continue
        timestamp = parse_iso_timestamp(timestamp_raw)
        record_type = record.get("type")
        payload = record.get("payload") or {}
        if record_type == "session_meta" and isinstance(payload, dict):
            session_id = payload.get("id") or session_id
            summary = (
                "The Codex Harness started a Codex session"
                f" in `{payload.get('cwd', 'unknown')}`"
            )
            cli_version = payload.get("cli_version")
            if isinstance(cli_version, str):
                summary += f" with CLI version `{cli_version}`"
            events.append(
                create_event(
                    timestamp=timestamp,
                    kind="session_started",
                    title="Session Started",
                    actor="Codex Harness",
                    summary=summary + ".",
                    source=source_label,
                    source_type="rollout",
                    session_id=session_id,
                    metadata={
                        "cwd": payload.get("cwd"),
                        "cli_version": payload.get("cli_version"),
                        "model_provider": payload.get("model_provider"),
                    },
                )
            )
            continue
        if record_type == "response_item" and isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type == "message":
                role = payload.get("role")
                text = extract_message_text(payload.get("content"))
                if role == "user" and text:
                    if is_bootstrap_prompt(text):
                        events.append(
                            create_event(
                                timestamp=timestamp,
                                kind="session_context",
                                title="Session Context Loaded",
                                actor="Codex Harness",
                                summary="The Codex Harness loaded session instructions and environment context.",
                                source=source_label,
                                source_type="rollout",
                                session_id=session_id,
                            )
                        )
                        continue
                    events.append(
                        create_event(
                            timestamp=timestamp,
                            kind="user_prompt",
                            title="Operator Prompt",
                            actor="the operator",
                            summary="The operator asked Codex a follow-on question.",
                            quote=text,
                            source=source_label,
                            source_type="rollout",
                            session_id=session_id,
                        )
                    )
                elif role == "assistant" and text:
                    events.append(
                        create_event(
                            timestamp=timestamp,
                            kind="assistant_message",
                            title="Codex Response",
                            actor="Codex",
                            summary="Codex responded to the operator.",
                            quote=text,
                            source=source_label,
                            source_type="rollout",
                            session_id=session_id,
                        )
                    )
                continue
            if payload_type == "reasoning":
                reasoning = extract_reasoning_text(payload)
                if reasoning:
                    events.append(
                        create_event(
                            timestamp=timestamp,
                            kind="reasoning",
                            title="Codex Reasoning",
                            actor="Codex",
                            summary="Codex recorded agent reasoning.",
                            quote=reasoning,
                            source=source_label,
                            source_type="rollout",
                            session_id=session_id,
                        )
                    )
                continue
            if payload_type == "function_call":
                tool_name = payload.get("name")
                raw_args = payload.get("arguments")
                args = parse_json_maybe(raw_args)
                command = extract_command(args)
                summary = f"The Codex Harness invoked `{tool_name}`."
                if command:
                    summary = f"The Codex Harness invoked `{tool_name}` with a command payload."
                approval = isinstance(args, dict) and args.get("sandbox_permissions") == "require_escalated"
                if approval:
                    summary = f"The Codex Harness requested approval before invoking `{tool_name}`."
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="tool_call",
                        title="Tool Call",
                        actor="Codex Harness",
                        summary=summary,
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                        call_id=payload.get("call_id"),
                        tool_name=tool_name,
                        command=command,
                        path_list=extract_patch_paths(raw_args if isinstance(raw_args, str) else None),
                        metadata={"arguments": args, "approval": approval},
                    )
                )
                continue
            if payload_type == "function_call_output":
                exit_code, output_text, changed_paths = parse_tool_output(payload.get("output"))
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="tool_result",
                        title="Tool Result",
                        actor="Codex Harness",
                        summary="The Codex Harness recorded tool output.",
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                        call_id=payload.get("call_id"),
                        output=output_text,
                        status=exit_code,
                        path_list=changed_paths,
                    )
                )
                continue
            if payload_type == "custom_tool_call":
                tool_name = payload.get("name")
                raw_input = payload.get("input")
                command = raw_input if isinstance(raw_input, str) else None
                title = "Patch Applied" if tool_name == "apply_patch" else "Custom Tool Call"
                summary = f"The Codex Harness invoked `{tool_name}`."
                if tool_name == "apply_patch":
                    summary = "The Codex Harness prepared an inline patch."
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="tool_call",
                        title=title,
                        actor="Codex Harness",
                        summary=summary,
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                        call_id=payload.get("call_id"),
                        tool_name=tool_name,
                        command=command,
                        path_list=extract_patch_paths(command),
                    )
                )
                continue
            if payload_type == "custom_tool_call_output":
                exit_code, output_text, changed_paths = parse_tool_output(payload.get("output"))
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="tool_result",
                        title="Custom Tool Result",
                        actor="Codex Harness",
                        summary="The Codex Harness recorded custom tool output.",
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                        call_id=payload.get("call_id"),
                        output=output_text,
                        status=exit_code,
                        path_list=changed_paths,
                    )
                )
                continue
            if payload_type == "web_search_call":
                action = payload.get("action")
                command = None
                summary = "The Codex Harness executed a web lookup."
                if isinstance(action, dict):
                    action_type = action.get("type")
                    if action_type == "search":
                        query = action.get("query")
                        if isinstance(query, str):
                            command = query
                            summary = f"The Codex Harness searched the web for `{query}`."
                    elif action_type == "open_page":
                        url = action.get("url")
                        if isinstance(url, str):
                            command = url
                            summary = f"The Codex Harness opened `{url}`."
                    elif action_type == "find_in_page":
                        needle = action.get("query")
                        url = action.get("url")
                        if isinstance(needle, str) and isinstance(url, str):
                            command = f"{needle} @ {url}"
                            summary = (
                                f"The Codex Harness searched `{url}` for `{needle}`."
                            )
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="web_lookup",
                        title="Web Lookup",
                        actor="Codex Harness",
                        summary=summary,
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                        tool_name="web_search_call",
                        command=command,
                    )
                )
                continue
        if record_type == "event_msg" and isinstance(payload, dict):
            event_type = payload.get("type")
            if event_type == "user_message" and isinstance(payload.get("message"), str):
                if is_bootstrap_prompt(payload["message"]):
                    events.append(
                        create_event(
                            timestamp=timestamp,
                            kind="session_context",
                            title="Session Context Loaded",
                            actor="Codex Harness",
                            summary="The Codex Harness loaded session instructions and environment context.",
                            source=source_label,
                            source_type="rollout",
                            session_id=session_id,
                        )
                    )
                    continue
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="user_prompt",
                        title="Operator Prompt",
                        actor="the operator",
                        summary="The operator asked Codex a follow-on question.",
                        quote=payload["message"],
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                    )
                )
            elif event_type == "agent_message" and isinstance(payload.get("message"), str):
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="assistant_message",
                        title="Codex Response",
                        actor="Codex",
                        summary="Codex responded to the operator.",
                        quote=payload["message"],
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                    )
                )
            elif event_type == "agent_reasoning" and isinstance(payload.get("text"), str):
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="reasoning",
                        title="Codex Reasoning",
                        actor="Codex",
                        summary="Codex recorded agent reasoning.",
                        quote=payload["text"],
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                    )
                )
            elif event_type == "task_started":
                task_name = payload.get("task") or payload.get("message") or "unknown task"
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="task_started",
                        title="Task Started",
                        actor="Codex Harness",
                        summary=f"The Codex Harness started `{task_name}`.",
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                    )
                )
            elif event_type == "task_complete":
                task_name = payload.get("task") or payload.get("message") or "unknown task"
                last_message = payload.get("last_agent_message")
                summary = f"The Codex Harness completed `{task_name}`."
                if isinstance(last_message, str) and normalize_ws(last_message):
                    summary += f" The last agent message began, \"{shorten(last_message, 140)}\"."
                events.append(
                    create_event(
                        timestamp=timestamp,
                        kind="task_complete",
                        title="Task Complete",
                        actor="Codex Harness",
                        summary=summary,
                        source=source_label,
                        source_type="rollout",
                        session_id=session_id,
                    )
                )
    return events


def parse_rollout_sources(
    codex_home: Path,
    include_archives: bool,
    stats: Counter,
) -> list[Event]:
    events: list[Event] = []
    sessions_dir = codex_home / "sessions"
    if not sessions_dir.exists():
        return events

    for path in sorted(sessions_dir.rglob("*.jsonl")):
        if path.name.startswith("._"):
            continue
        stats["rollout_files"] += 1
        source_label = f"rollout::{path.relative_to(codex_home)}"
        events.extend(
            parse_rollout_events(
                path.read_text(encoding="utf-8", errors="replace").splitlines(),
                source_label,
                path.name,
                stats,
            )
        )

    if not include_archives:
        return events

    for archive in sorted(sessions_dir.rglob("*.zip")):
        stats["rollout_archives"] += 1
        with zipfile.ZipFile(archive) as zf:
            for member in sorted(zf.namelist()):
                if member.startswith("__MACOSX/") or member.endswith("/") or not member.endswith(".jsonl"):
                    continue
                stats["rollout_members"] += 1
                source_label = f"archive::{archive.relative_to(codex_home)}::{member}"
                with zf.open(member) as handle:
                    raw = handle.read().decode("utf-8", errors="replace")
                events.extend(
                    parse_rollout_events(
                        raw.splitlines(),
                        source_label,
                        Path(member).name,
                        stats,
                    )
                )
    return events


def parse_history(codex_home: Path, stats: Counter) -> list[Event]:
    history_path = codex_home / "history.jsonl"
    if not history_path.exists():
        return []
    stats["history_files"] += 1
    events: list[Event] = []
    for line in history_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            stats["history_decode_errors"] += 1
            continue
        ts = record.get("ts")
        text = record.get("text")
        if not isinstance(ts, (int, float)) or not isinstance(text, str):
            continue
        if is_bootstrap_prompt(text):
            continue
        timestamp = datetime.fromtimestamp(float(ts), tz=UTC)
        events.append(
            create_event(
                timestamp=timestamp,
                kind="user_prompt",
                title="Operator Prompt",
                actor="the operator",
                summary="The operator asked Codex a follow-on question.",
                quote=text,
                source=f"history::{history_path.relative_to(codex_home)}",
                source_type="history",
                session_id=record.get("session_id"),
            )
        )
    return events


def split_tui_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    lines: list[str] = []
    for raw_line in text.splitlines():
        match = TIMESTAMP_RE.match(raw_line)
        if match:
            if current is not None:
                current["message"] = "\n".join(lines)
                records.append(current)
            current = {
                "ts": match.group("ts"),
                "level": match.group("level"),
            }
            lines = [match.group("rest")]
            continue
        if current is not None:
            lines.append(raw_line)
    if current is not None:
        current["message"] = "\n".join(lines)
        records.append(current)
    return records


def parse_json_payload_from_text(text: str) -> tuple[Any, str]:
    stripped = text.strip()
    if not stripped.startswith("{"):
        return None, stripped
    decoder = json.JSONDecoder()
    try:
        obj, end = decoder.raw_decode(stripped)
    except json.JSONDecodeError:
        return None, stripped
    remainder = stripped[end:].strip()
    return obj, remainder


def parse_tui_message(
    *,
    timestamp: datetime,
    level: str,
    message: str,
    source: str,
    source_type: str,
    session_id: str | None,
) -> list[Event]:
    events: list[Event] = []
    if "ToolCall:" in message:
        suffix = message.split("ToolCall:", 1)[1].strip()
        tool_name, _, remainder = suffix.partition(" ")
        args, trailing = parse_json_payload_from_text(remainder)
        command = extract_command(args)
        title = "Patch Applied" if tool_name == "apply_patch" else "Tool Call"
        summary = f"The Codex Harness invoked `{tool_name}`."
        if command:
            summary = f"The Codex Harness invoked `{tool_name}` with a command payload."
        approval = isinstance(args, dict) and args.get("sandbox_permissions") == "require_escalated"
        if approval:
            summary = f"The Codex Harness requested approval before invoking `{tool_name}`."
        patch_text = None
        if tool_name == "apply_patch":
            patch_text = remainder if remainder else trailing
        events.append(
            create_event(
                timestamp=timestamp,
                kind="tool_call",
                title=title,
                actor="Codex Harness",
                summary=summary,
                source=source,
                source_type=source_type,
                session_id=session_id,
                tool_name=tool_name,
                command=command or patch_text,
                path_list=extract_patch_paths(patch_text),
                metadata={"arguments": args, "approval": approval},
            )
        )
        return events

    if level in {"WARN", "ERROR"}:
        target = message.split(":", 1)[0]
        events.append(
            create_event(
                timestamp=timestamp,
                kind="warning" if level == "WARN" else "error",
                title=f"{level} Logged",
                actor="Codex Harness",
                summary=f"Codex logged a {level} from `{target}`.",
                source=source,
                source_type=source_type,
                session_id=session_id,
                level=level,
                output=message,
            )
        )
        return events

    if "Shutting down Codex instance" in message:
        events.append(
            create_event(
                timestamp=timestamp,
                kind="session_stopped",
                title="Session Stopped",
                actor="Codex Harness",
                summary="The Codex Harness shut down a Codex instance.",
                source=source,
                source_type=source_type,
                session_id=session_id,
            )
        )
    return events


def parse_tui_log(codex_home: Path, stats: Counter) -> list[Event]:
    log_path = codex_home / "log" / "codex-tui.log"
    if not log_path.exists():
        return []
    stats["tui_logs"] += 1
    events: list[Event] = []
    records = split_tui_records(log_path.read_text(encoding="utf-8", errors="replace"))
    for record in records:
        timestamp = parse_iso_timestamp(record["ts"])
        message = record["message"]
        match = THREAD_ID_RE.search(message)
        session_id = match.group(1) if match else None
        source = f"tui::{log_path.relative_to(codex_home)}"
        events.extend(
            parse_tui_message(
                timestamp=timestamp,
                level=record["level"],
                message=message,
                source=source,
                source_type="tui_log",
                session_id=session_id,
            )
        )
    return events


def parse_sqlite_logs(codex_home: Path, stats: Counter) -> list[Event]:
    events: list[Event] = []
    for db_path in sorted(codex_home.glob("logs*.sqlite")):
        stats["sqlite_dbs"] += 1
        try:
            connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        except sqlite3.Error:
            stats["sqlite_open_errors"] += 1
            continue
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT ts, ts_nanos, level, target, message, thread_id
                FROM logs
                WHERE level IN ('WARN', 'ERROR')
                   OR message LIKE '%ToolCall:%'
                   OR message LIKE '%Shutting down Codex instance%'
                ORDER BY ts ASC, ts_nanos ASC, id ASC
                """
            )
            for ts, ts_nanos, level, target, message, thread_id in cursor.fetchall():
                if not isinstance(ts, int) or not isinstance(ts_nanos, int):
                    continue
                timestamp = datetime.fromtimestamp(ts, tz=UTC) + timedelta(
                    microseconds=ts_nanos // 1000
                )
                combined = f"{target}: {message or ''}".strip()
                source = f"sqlite::{db_path.relative_to(codex_home)}"
                events.extend(
                    parse_tui_message(
                        timestamp=timestamp,
                        level=level,
                        message=combined,
                        source=source,
                        source_type="sqlite",
                        session_id=thread_id,
                    )
                )
    return events


def summarize_task_snapshot(tasks: Any) -> str:
    if not isinstance(tasks, list):
        return "The Codex Harness recorded planner task state."
    count = len(tasks)
    if count == 0:
        return "The Codex Harness recorded an empty planner task snapshot."
    fragments: list[str] = []
    for task in tasks[:3]:
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id", "unknown-task")
        status = task.get("status", "unknown")
        fragments.append(f"`{task_id}` as `{status}`")
    joined = ", ".join(fragments)
    if count > 3:
        joined += f", plus {count - 3} more task(s)"
    return f"The Codex Harness recorded {count} planner task(s): {joined}."


def parse_state_artifacts(codex_home: Path, stats: Counter) -> list[Event]:
    state_dir = codex_home / "state"
    if not state_dir.exists():
        return []
    events: list[Event] = []
    for run_dir in sorted(path for path in state_dir.iterdir() if path.is_dir()):
        stats["state_runs"] += 1
        run_name = run_dir.name
        tasks_path = run_dir / "tasks.json"
        if tasks_path.exists():
            stats["state_files"] += 1
            try:
                tasks = json.loads(tasks_path.read_text(encoding="utf-8", errors="replace"))
            except json.JSONDecodeError:
                tasks = None
            events.append(
                create_event(
                    timestamp=datetime.fromtimestamp(tasks_path.stat().st_mtime, tz=UTC),
                    kind="planner_tasks_snapshot",
                    title="Planner Tasks Snapshot",
                    actor="Codex Harness",
                    summary=summarize_task_snapshot(tasks),
                    source=f"state::{tasks_path.relative_to(codex_home)}",
                    source_type="state",
                    metadata={"mtime_derived": True, "run_id": run_name},
                )
            )
        evidence_path = run_dir / "evidence-index.json"
        if evidence_path.exists():
            stats["state_files"] += 1
            try:
                evidence = json.loads(
                    evidence_path.read_text(encoding="utf-8", errors="replace")
                )
            except json.JSONDecodeError:
                evidence = {}
            count = len(evidence) if isinstance(evidence, dict) else 0
            events.append(
                create_event(
                    timestamp=datetime.fromtimestamp(evidence_path.stat().st_mtime, tz=UTC),
                    kind="planner_evidence_snapshot",
                    title="Evidence Snapshot",
                    actor="Codex Harness",
                    summary=f"The Codex Harness recorded {count} evidence item(s) for planner run `{run_name}`.",
                    source=f"state::{evidence_path.relative_to(codex_home)}",
                    source_type="state",
                    metadata={"mtime_derived": True, "run_id": run_name},
                )
            )
        agent_results_dir = run_dir / "agent-results"
        if agent_results_dir.exists():
            for result_path in sorted(agent_results_dir.glob("*.json")):
                stats["state_files"] += 1
                try:
                    result = json.loads(result_path.read_text(encoding="utf-8", errors="replace"))
                except json.JSONDecodeError:
                    result = {}
                objective = result.get("objective", "unknown objective")
                findings = result.get("findings")
                finding_count = len(findings) if isinstance(findings, list) else 0
                command_results = result.get("command_results")
                command_count = (
                    len(command_results) if isinstance(command_results, list) else 0
                )
                agent_name = result_path.stem.split("-task-", 1)[0].replace("_", " ")
                events.append(
                    create_event(
                        timestamp=datetime.fromtimestamp(result_path.stat().st_mtime, tz=UTC),
                        kind="agent_result",
                        title="Agent Result Saved",
                        actor="Codex Harness",
                        summary=(
                            f"The Codex Harness saved a {agent_name} result for `{objective}`"
                            f" with {command_count} command result(s) and {finding_count} finding(s)."
                        ),
                        source=f"state::{result_path.relative_to(codex_home)}",
                        source_type="state",
                        metadata={"mtime_derived": True, "run_id": run_name},
                    )
                )
    return events


def deduplicate_events(events: list[Event]) -> list[Event]:
    deduped: dict[tuple[str, str, str, str, str], Event] = {}
    for event in events:
        signature = event_signature(event)
        existing = deduped.get(signature)
        if existing is None or should_keep_better(existing, event):
            deduped[signature] = event
    return sorted(deduped.values())


def merge_tool_events(events: list[Event]) -> list[Event]:
    result_by_call: dict[str, deque[Event]] = defaultdict(deque)
    for event in events:
        if event.kind == "tool_result" and event.call_id:
            result_by_call[event.call_id].append(event)

    merged: list[Event] = []
    consumed_results: set[int] = set()
    seen_calls: set[str] = set()

    for event in events:
        if event.kind == "tool_result" and event.call_id:
            if id(event) in consumed_results or event.call_id in seen_calls:
                continue
        if event.kind != "tool_call" or not event.call_id:
            if event.kind != "tool_result":
                merged.append(event)
            elif not event.call_id:
                merged.append(event)
            continue

        seen_calls.add(event.call_id)
        queue = result_by_call.get(event.call_id)
        match: Event | None = None
        while queue:
            candidate = queue.popleft()
            if candidate.session_id and event.session_id and candidate.session_id != event.session_id:
                continue
            if candidate.timestamp < event.timestamp:
                continue
            consumed_results.add(id(candidate))
            match = candidate
            break

        if match is None:
            merged.append(event)
            continue

        title = "Patch Applied" if event.tool_name == "apply_patch" else "Tool Execution"
        summary = event.summary
        if event.tool_name == "apply_patch" and event.path_list:
            summary = (
                "The Codex Harness applied a patch that touched "
                + ", ".join(f"`{path}`" for path in event.path_list)
                + "."
            )
        elif event.command:
            summary = f"The Codex Harness executed `{event.tool_name}`."
        approval = bool(event.metadata.get("approval"))
        if approval:
            summary = f"The Codex Harness requested approval to execute `{event.tool_name}`."

        merged.append(
            create_event(
                timestamp=event.timestamp,
                kind="tool_execution",
                title=title,
                actor="Codex Harness",
                summary=summary,
                source=event.source,
                source_type=event.source_type,
                session_id=event.session_id,
                call_id=event.call_id,
                tool_name=event.tool_name,
                command=event.command,
                output=match.output,
                status=match.status,
                path_list=event.path_list or match.path_list,
                metadata={**event.metadata, **match.metadata},
            )
        )

    for event in events:
        if event.kind == "tool_result" and event.call_id and id(event) not in consumed_results:
            merged.append(event)

    return sorted(merged)


def remove_shadowed_tool_calls(events: list[Event]) -> list[Event]:
    executions = [
        event
        for event in events
        if event.kind == "tool_execution"
    ]
    filtered: list[Event] = []
    for event in events:
        if event.kind != "tool_call":
            filtered.append(event)
            continue
        shadowed = False
        for execution in executions:
            if execution.session_id != event.session_id:
                continue
            if execution.tool_name != event.tool_name:
                continue
            if abs((execution.timestamp - event.timestamp).total_seconds()) > 1:
                continue
            if event.command and execution.command and normalize_ws(event.command) == normalize_ws(execution.command):
                shadowed = True
                break
            if event.path_list and execution.path_list and event.path_list == execution.path_list:
                shadowed = True
                break
        if not shadowed:
            filtered.append(event)
    return filtered


def command_segment_is_read_only(segment: str) -> bool:
    segment = segment.strip()
    if not segment:
        return True
    if COMMAND_WRITE_RE.search(segment):
        return False
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return False
    if not tokens:
        return True
    command = tokens[0]
    lower = segment.lower()
    if command in {"git"}:
        return len(tokens) > 1 and tokens[1] in {"branch", "diff", "log", "rev-parse", "show", "status"}
    if command in {"docker", "docker-compose"}:
        if len(tokens) <= 1:
            return False
        if command == "docker" and tokens[1] == "compose":
            return len(tokens) > 2 and tokens[2] in {"config", "logs", "ps"}
        return tokens[1] in {"config", "inspect", "logs", "ps"}
    if command == "sqlite3":
        return not re.search(r"\b(update|insert|delete|create|drop|alter|attach|vacuum|pragma)\b", lower)
    if command == "unzip":
        return "-l" in tokens or "-p" in tokens
    if command not in READ_ONLY_COMMANDS:
        return False
    redirection_match = re.search(r"(^|[^0-9])>>?|[0-9]>>?", segment)
    if redirection_match and "/dev/null" not in segment:
        return False
    return True


def is_read_only_command(command: str | None) -> bool:
    if not command:
        return False
    segments = re.split(r"\s*(?:&&|\|\||;)\s*", command)
    return all(command_segment_is_read_only(segment) for segment in segments)


def collapse_events(events: list[Event]) -> list[Event]:
    collapsed: list[Event] = []
    index = 0
    while index < len(events):
        event = events[index]
        if (
            event.kind in {"tool_execution", "tool_call"}
            and event.command
            and is_read_only_command(event.command)
        ):
            batch = [event]
            j = index + 1
            while j < len(events):
                candidate = events[j]
                if candidate.kind not in {"tool_execution", "tool_call"}:
                    break
                if candidate.session_id != event.session_id:
                    break
                if not candidate.command or not is_read_only_command(candidate.command):
                    break
                if candidate.timestamp - batch[-1].timestamp > timedelta(seconds=20):
                    break
                batch.append(candidate)
                j += 1
            if len(batch) >= 2:
                commands = [item.command for item in batch if item.command]
                collapsed.append(
                    create_event(
                        timestamp=batch[0].timestamp,
                        kind="inspection_batch",
                        title="Read-Only Inspection",
                        actor="Codex Harness",
                        summary=f"The Codex Harness ran {len(commands)} read-only inspection command(s).",
                        source=batch[0].source,
                        source_type=batch[0].source_type,
                        session_id=batch[0].session_id,
                        metadata={"commands": commands},
                    )
                )
                index = j
                continue
        if event.tool_name == "write_stdin" and not normalize_ws(event.command):
            count = 1
            j = index + 1
            while j < len(events):
                candidate = events[j]
                if candidate.tool_name != "write_stdin" or normalize_ws(candidate.command):
                    break
                if candidate.session_id != event.session_id:
                    break
                if candidate.timestamp - event.timestamp > timedelta(seconds=60):
                    break
                count += 1
                j += 1
            if count > 1:
                collapsed.append(
                    create_event(
                        timestamp=event.timestamp,
                        kind="pty_poll_batch",
                        title="PTY Polling",
                        actor="Codex Harness",
                        summary=f"The Codex Harness polled an active PTY session {count} times.",
                        source=event.source,
                        source_type=event.source_type,
                        session_id=event.session_id,
                    )
                )
                index = j
                continue
        collapsed.append(event)
        index += 1
    return collapsed


def filter_events(events: list[Event], session_id: str | None) -> list[Event]:
    if not session_id:
        return events
    filtered: list[Event] = []
    for event in events:
        if event.session_id == session_id:
            filtered.append(event)
    return filtered


def event_text_for_matching(event: Event) -> str:
    parts: list[str] = [
        event.title,
        event.summary,
        event.actor,
        event.source,
        event.tool_name or "",
        event.command or "",
        event.quote or "",
        event.output or "",
    ]
    parts.extend(event.path_list)
    metadata_commands = event.metadata.get("commands")
    if isinstance(metadata_commands, list):
        parts.extend(str(command) for command in metadata_commands)
    return "\n".join(part for part in parts if part)


def focus_events_by_pattern(events: list[Event], patterns: list[str]) -> list[Event]:
    if not patterns:
        return events

    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    seeded_sessions: set[str] = set()
    direct_matches: set[int] = set()

    for event in events:
        haystack = event_text_for_matching(event)
        if any(pattern.search(haystack) for pattern in compiled):
            direct_matches.add(id(event))
            if event.session_id:
                seeded_sessions.add(event.session_id)

    focused: list[Event] = []
    for event in events:
        if id(event) in direct_matches:
            focused.append(event)
            continue
        if event.session_id and event.session_id in seeded_sessions:
            focused.append(event)

    return focused


def command_block(commands: list[str]) -> list[str]:
    lines = ["```sh"]
    lines.extend(commands)
    lines.append("```")
    return lines


def quoted_block(text: str) -> list[str]:
    return [f"> {line}" if line else ">" for line in text.splitlines()]


def describe_result(event: Event) -> str | None:
    parts: list[str] = []
    if event.status:
        parts.append(f"exit `{event.status}`")
    if event.output:
        excerpt = shorten(event.output, 320)
        if excerpt:
            parts.append(f"output excerpt: `{excerpt}`")
    if event.path_list:
        parts.append(
            "files: " + ", ".join(f"`{path}`" for path in event.path_list)
        )
    if not parts:
        return None
    return "; ".join(parts)


def render_timeline(
    events: list[Event],
    *,
    repo_root: Path,
    codex_home: Path,
    stats: Counter,
    generated_at: datetime,
) -> str:
    lines = [
        "# Codex Timeline",
        "",
        f"Generated: {format_timestamp(generated_at)}",
        f"Repository Root: `{repo_root}`",
        f"Codex Home: `{codex_home}`",
        "Timezone: `UTC` only",
        "",
        "## Source Coverage",
        "",
        f"- Rollout JSONL files: {stats['rollout_files']}",
        f"- Archived rollout members: {stats['rollout_members']}",
        f"- Session archives scanned: {stats['rollout_archives']}",
        f"- History files: {stats['history_files']}",
        f"- TUI logs: {stats['tui_logs']}",
        f"- SQLite log databases: {stats['sqlite_dbs']}",
        f"- Planner state runs: {stats['state_runs']}",
        f"- Rendered timeline events: {len(events)}",
        "",
        "## Normalization Notes",
        "",
        "- Rollout JSONL data takes precedence when it overlaps with TUI, history, or SQLite records.",
        "- The timeline groups repetitive read-only inspection commands and PTY polling to keep the chronology readable.",
        "- Planner state artifacts use filesystem modification time when the artifact lacks an embedded timestamp.",
        "",
        "## Chronology",
        "",
    ]

    for event in events:
        lines.append(f"### {format_timestamp(event.timestamp)} | {event.title}")
        if event.session_id:
            lines.append(f"Session: `{event.session_id}`")
        lines.append(f"Actor: {event.actor}")
        lines.append(f"Source: `{event.source}`")
        lines.append(f"Summary: {event.summary}")
        if event.quote:
            lines.append("Quote:")
            lines.extend(quoted_block(event.quote))
        commands = event.metadata.get("commands")
        if isinstance(commands, list) and commands:
            lines.append("Commands:")
            lines.extend(command_block(commands))
        elif event.command:
            lines.append("Command:")
            lines.extend(command_block([event.command]))
        result_text = describe_result(event)
        if result_text:
            lines.append(f"Result: {result_text}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def summarize_assistant_text(text: str) -> str:
    cleaned = normalize_ws(text)
    if len(cleaned) <= 180:
        return f'Codex replied, "{cleaned}".'
    return f'Codex responded with guidance that began, "{shorten(cleaned, 180)}".'


def summarize_reasoning_text(text: str) -> str:
    cleaned = normalize_ws(text)
    return f'Codex reasoned, "{shorten(cleaned, 200)}".'


def summarize_command_list(commands: list[str]) -> str:
    return "; ".join(f"`{command}`" for command in commands)


def render_narrative_sentence(event: Event, include_day: bool) -> str:
    prefix = narrative_prefix(event.timestamp, include_day)
    if event.kind == "session_started":
        cwd = event.metadata.get("cwd")
        if isinstance(cwd, str):
            return f"{prefix}, the Codex Harness started a session in `{cwd}`."
        return f"{prefix}, the Codex Harness started a Codex session."
    if event.kind == "session_context":
        return f"{prefix}, the Codex Harness loaded session instructions and environment context."
    if event.kind == "session_stopped":
        return f"{prefix}, the Codex Harness shut down a Codex session."
    if event.kind == "user_prompt" and event.quote:
        return f'{prefix}, the operator asked Codex, "{normalize_ws(event.quote)}".'
    if event.kind == "assistant_message" and event.quote:
        return f"{prefix}, {summarize_assistant_text(event.quote)}"
    if event.kind == "reasoning" and event.quote:
        return f"{prefix}, {summarize_reasoning_text(event.quote)}"
    if event.kind == "inspection_batch":
        commands = event.metadata.get("commands")
        if isinstance(commands, list) and commands:
            return (
                f"{prefix}, the Codex Harness inspected local artifacts with "
                f"{len(commands)} read-only command(s): {summarize_command_list(commands)}."
            )
        return f"{prefix}, the Codex Harness inspected local artifacts."
    if event.kind == "pty_poll_batch":
        return f"{prefix}, the Codex Harness polled an active PTY session repeatedly."
    if event.kind == "tool_execution":
        approval = bool(event.metadata.get("approval"))
        if approval and event.command:
            justification = None
            arguments = event.metadata.get("arguments")
            if isinstance(arguments, dict) and isinstance(arguments.get("justification"), str):
                justification = normalize_ws(arguments["justification"])
            sentence = (
                f"{prefix}, the Codex Harness requested approval to run `{event.command}`."
            )
            if justification:
                sentence += f' The justification read, "{justification}".'
            return sentence
        if event.tool_name == "apply_patch":
            sentence = f"{prefix}, the Codex Harness applied a patch"
            if event.path_list:
                sentence += " to " + ", ".join(f"`{path}`" for path in event.path_list)
            sentence += "."
            result_text = describe_result(event)
            if result_text:
                sentence += f" The result was {result_text}."
            return sentence
        if event.command:
            sentence = f"{prefix}, the Codex Harness executed `{event.command}`."
        else:
            sentence = f"{prefix}, the Codex Harness executed `{event.tool_name}`."
        result_text = describe_result(event)
        if result_text:
            sentence += f" The result was {result_text}."
        return sentence
    if event.kind == "planner_tasks_snapshot":
        return f"{prefix}, {event.summary}"
    if event.kind == "planner_evidence_snapshot":
        return f"{prefix}, {event.summary}"
    if event.kind == "agent_result":
        return f"{prefix}, {event.summary}"
    if event.kind == "web_lookup" and event.command:
        return f"{prefix}, the Codex Harness executed a web lookup for `{event.command}`."
    if event.kind == "task_started":
        return f"{prefix}, {event.summary}"
    if event.kind == "task_complete":
        return f"{prefix}, {event.summary}"
    if event.kind in {"warning", "error"} and event.output:
        return (
            f'{prefix}, Codex logged a {event.level} event: "{shorten(event.output, 220)}".'
        )
    if event.command:
        return f"{prefix}, the Codex Harness ran `{event.command}`."
    return f"{prefix}, {event.summary}"


def chunk_sentences(sentences: list[str], chunk_size: int = 6) -> list[str]:
    chunks: list[str] = []
    for index in range(0, len(sentences), chunk_size):
        chunks.append(" ".join(sentences[index : index + chunk_size]))
    return chunks


def render_narrative(
    events: list[Event],
    *,
    repo_root: Path,
    codex_home: Path,
    stats: Counter,
    generated_at: datetime,
) -> str:
    lines = [
        "# Codex Narrative",
        "",
        f"Generated: {format_timestamp(generated_at)}",
        f"Repository Root: `{repo_root}`",
        f"Codex Home: `{codex_home}`",
        "Timezone: `UTC` only",
        "",
        "## Coverage",
        "",
        "- This narrative uses the same normalized event set as the timeline.",
        "- Rollout JSONL files provide the primary chronology when available.",
        "- Planner state timestamps come from file modification time when the artifacts do not embed their own time fields.",
        "",
    ]

    by_day: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        key = event.timestamp.astimezone(UTC).strftime("%Y-%m-%d")
        by_day[key].append(event)

    for day_key in sorted(by_day):
        day_events = by_day[day_key]
        day_header = day_events[0].timestamp.astimezone(UTC)
        lines.append(f"## {day_header.strftime('%B')} {day_header.day}, {day_header.year}")
        lines.append("")
        sentences: list[str] = []
        for index, event in enumerate(day_events):
            sentences.append(render_narrative_sentence(event, include_day=index == 0))
        lines.extend(chunk_sentences(sentences))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_report(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    codex_home = (args.codex_home or (repo_root / ".codex")).resolve()
    output_dir = (args.output_dir or (repo_root / "reports")).resolve()

    if not codex_home.exists():
        print(f"[ERROR] Codex home does not exist: {codex_home}", file=sys.stderr)
        return 1

    stats: Counter = Counter()
    generated_at = datetime.now(tz=UTC)

    events: list[Event] = []
    events.extend(parse_rollout_sources(codex_home, not args.no_archives, stats))
    events.extend(parse_history(codex_home, stats))
    events.extend(parse_tui_log(codex_home, stats))
    events.extend(parse_sqlite_logs(codex_home, stats))
    events.extend(parse_state_artifacts(codex_home, stats))

    events = deduplicate_events(events)
    events = merge_tool_events(events)
    events = remove_shadowed_tool_calls(events)
    events = collapse_events(events)
    events = deduplicate_events(events)
    events = filter_events(events, args.session_id)
    events = focus_events_by_pattern(events, args.focus_pattern)

    if not events:
        print("[ERROR] No Codex events were parsed from the supplied artifacts.", file=sys.stderr)
        return 1

    timeline_path = output_dir / args.timeline_name
    narrative_path = output_dir / args.narrative_name

    write_report(
        timeline_path,
        render_timeline(
            events,
            repo_root=repo_root,
            codex_home=codex_home,
            stats=stats,
            generated_at=generated_at,
        ),
    )
    write_report(
        narrative_path,
        render_narrative(
            events,
            repo_root=repo_root,
            codex_home=codex_home,
            stats=stats,
            generated_at=generated_at,
        ),
    )

    print(f"[OK] Wrote timeline: {timeline_path}")
    print(f"[OK] Wrote narrative: {narrative_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
