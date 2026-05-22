---
name: ghostwriter-mcp
description: Use for Ghostwriter MCP setup, connection verification, project discovery, oplog discovery, and environment guidance in Codex.
---

# Ghostwriter MCP

Use this skill when the user wants to configure or verify Ghostwriter MCP access from Codex, list Ghostwriter projects, select an operation log, or troubleshoot Ghostwriter MCP startup.

## Runtime Requirements

The Codex plugin exposes the `ghostwriter` MCP server through `../../.mcp.json` and `../../scripts/run-ghostwriter-mcp.sh`.

Required environment:

- `GHOSTWRITER_MCP_DIR` or an installed server at `vendor/ghostwriter-mcp`
- `GHOSTWRITER_URL`
- `GHOSTWRITER_API_KEY`
- `GHOSTWRITER_CA_BUNDLE` when the Ghostwriter deployment uses a private CA

Install server dependencies with:

```bash
GHOSTWRITER_MCP_SOURCE=<git-url-or-local-path> plugins/report-writing/scripts/install-ghostwriter-mcp-deps.sh
```

## Workflow

1. If MCP tools are unavailable, check whether the plugin is installed and whether `GHOSTWRITER_MCP_DIR` points to a valid Ghostwriter MCP server checkout.
2. If the server is missing, tell the user to run `scripts/install-ghostwriter-mcp-deps.sh` with `GHOSTWRITER_MCP_SOURCE` or `--source`.
3. Verify credentials with the Ghostwriter MCP `whoami` tool when available.
4. For project selection, use `list_projects` with active projects first and summarize project ID, codename, client, and dates.
5. For oplog selection, inspect the selected project's oplogs and return the chosen oplog ID/name.
6. Tell the user to export or configure the chosen values for downstream oplog workflows:
   - `GHOSTWRITER_PROJECT_ID`
   - `GHOSTWRITER_OPLOG_ID`
   - `GHOSTWRITER_OPERATOR`

## Troubleshooting

- Missing `uv`: install `uv` and restart Codex.
- Missing server directory: run `scripts/install-ghostwriter-mcp-deps.sh` or set `GHOSTWRITER_MCP_DIR`.
- Authentication failure: verify `GHOSTWRITER_URL`, `GHOSTWRITER_API_KEY`, and CA bundle settings.
- Private CA failures: set `GHOSTWRITER_CA_BUNDLE` to the CA bundle path used by the Ghostwriter deployment.
