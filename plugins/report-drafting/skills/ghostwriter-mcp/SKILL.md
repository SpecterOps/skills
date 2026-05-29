---
name: ghostwriter-mcp
description: Use for Ghostwriter MCP setup, connection verification, project discovery, oplog discovery, and environment guidance in Codex.
metadata:
  author: "GhostWorks"
---

# Ghostwriter MCP

Use this skill when the user wants to configure or verify Ghostwriter MCP access from Codex, list Ghostwriter projects, select an operation log, or troubleshoot Ghostwriter MCP startup.

## Runtime Requirements

Codex should be configured directly with a `mcp_servers.ghostwriter` entry that runs the external Ghostwriter MCP server, for example `uv --directory /path/to/GhostWriterMCP run python -m ghostwritermcp.server`.

Required environment:

- `GHOSTWRITER_URL`
- `GHOSTWRITER_API_KEY`
- `GHOSTWRITER_CA_BUNDLE` when the Ghostwriter deployment uses a private CA

## Workflow

1. If MCP tools are unavailable, check whether Codex has a direct `mcp_servers.ghostwriter` entry with the correct `command`, `args`, and environment values.
2. If the server is missing, tell the user to install or clone GhostWriterMCP and configure Codex to run it directly.
3. Verify credentials with the Ghostwriter MCP `whoami` tool when available.
4. For project selection, use `list_projects` with active projects first and summarize project ID, codename, client, and dates.
5. For oplog selection, inspect the selected project's oplogs and return the chosen oplog ID/name.
6. Tell the user to export or configure the chosen values for downstream oplog workflows:
   - `GHOSTWRITER_PROJECT_ID`
   - `GHOSTWRITER_OPLOG_ID`
   - `GHOSTWRITER_OPERATOR`

## Troubleshooting

- Missing `uv`: install `uv` and restart Codex.
- Missing server command or checkout: install or clone GhostWriterMCP and update `mcp_servers.ghostwriter`.
- Authentication failure: verify `GHOSTWRITER_URL`, `GHOSTWRITER_API_KEY`, and CA bundle settings.
- Private CA failures: set `GHOSTWRITER_CA_BUNDLE` to the CA bundle path used by the Ghostwriter deployment.
