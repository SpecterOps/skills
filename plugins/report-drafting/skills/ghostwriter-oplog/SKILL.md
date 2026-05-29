---
name: ghostwriter-oplog
description: Use for Ghostwriter operation log entries from Codex, including config guidance, quick notes, evidence-backed entries, and guided oplog capture through the Ghostwriter MCP tools.
metadata:
  author: "GhostWorks"
---

# Ghostwriter Oplog

Use this skill when the user wants to create Ghostwriter operation log entries from Codex.

## Inputs

Accept one of these actions:

- `config` — show required environment variables and current expected names.
- `quick <description> [--tags tag1,tag2]` — create a timestamped entry.
- `evidence <file-path> <description> [--tags tag1,tag2]` — create an entry with file contents or a binary-file note.
- `guided` — ask for entry type, description, optional evidence, destination, tool, and tags before logging.

## Environment

Preferred variables:

- `GHOSTWRITER_OPLOG_ID`
- `GHOSTWRITER_OPERATOR`
- `GHOSTWRITER_SOURCE_IP` optional

Accepted legacy aliases:

- `GW_OPLOG_ID`
- `GW_OPERATOR_NAME`
- `GW_SOURCE_IP`

If required values are missing, do not guess. Tell the user to set the preferred variables in their shell or Codex environment and restart Codex if needed.

## Logging Workflow

1. Resolve `oplog_id` from `GHOSTWRITER_OPLOG_ID` or `GW_OPLOG_ID`.
2. Resolve `operator_name` from `GHOSTWRITER_OPERATOR` or `GW_OPERATOR_NAME`.
3. Resolve optional `source_ip` from `GHOSTWRITER_SOURCE_IP` or `GW_SOURCE_IP`.
4. Get a UTC timestamp with `date -u +"%Y-%m-%dT%H:%M:%SZ"`.
5. Use the Ghostwriter MCP `create_oplog_entry` tool with resolved fields.
6. Confirm the entry ID and summarize the fields recorded.

## Action Details

### quick

Parse everything before `--tags` as the description. Parse tags as a comma-separated list. Submit `description`, `start_date`, optional `tags`, and resolved operator/source fields.

### evidence

Read the provided file path. If it is text, include file contents as `output`. If it appears binary or cannot be decoded safely, set `output` to `[Binary file: <path>]` and include the file path in the description.

### guided

Collect:

- entry type: command execution, discovery, credential access, or evidence capture
- description
- optional evidence file path
- optional destination IP/hostname
- optional tool name
- optional tags

Then submit the completed entry through `create_oplog_entry`.

### config

Show this minimum configuration:

```bash
export GHOSTWRITER_OPLOG_ID=<oplog-id>
export GHOSTWRITER_OPERATOR=<operator-name>
export GHOSTWRITER_SOURCE_IP=<source-ip> # optional
```

If the user needs to discover projects or oplogs first, use the `ghostwriter-mcp` skill to verify the MCP connection and list projects/oplogs.
