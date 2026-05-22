# Ghostwriter MCP Plugin

Claude Code plugin for Ghostwriter security documentation platform.

## Prerequisites

- [UV](https://docs.astral.sh/uv/) package manager
- Running Ghostwriter instance


## MCP packaging

This plugin includes Codex MCP configuration plus plugin-local install/run scripts for the Ghostwriter MCP server.

- `.mcp.json` points Codex at the plugin-owned MCP runner.
- `scripts/install-mcp-deps.sh` installs or updates the Ghostwriter MCP checkout under `vendor/ghostwriter-mcp` by default.
- `scripts/run-ghostwriter-mcp.sh` runs the server from `GHOSTWRITER_MCP_DIR` or the plugin-local vendor directory, and auto-runs the installer on first start when the checkout is missing.
- `mcp/env.example` documents required Ghostwriter connection variables without committing secrets.

The first MCP start bootstraps the plugin-local server checkout automatically unless `GHOSTWRITER_MCP_AUTO_INSTALL=0` is set.

## Codex GUI app setup

After installing `ghostwriter-mcp` from the Codex GUI `/plugins` view, add Ghostwriter connection values to `~/.codex/config.toml` so the GUI app can see them, then fully restart Codex. The plugin-owned MCP runner clones/syncs `https://github.com/SpecterOps/GhostWriterMCP.git` into `vendor/ghostwriter-mcp` on first start.

```toml
[mcp_servers.ghostwriter.env]
GHOSTWRITER_URL = "https://ghostwriter.example.com/"
GHOSTWRITER_API_KEY = "YOUR_API_KEY"
GHOSTWRITER_CA_BUNDLE = "/path/to/ca-bundle.crt"
```

If you also use `ghostwriter-oplog`, add oplog defaults to the same env block:

```toml
GHOSTWRITER_OPLOG_ID = "123"
GHOSTWRITER_OPERATOR = "your-callsign"
GHOSTWRITER_SOURCE_IP = "10.0.0.5"
```


#### Windows native PowerShell wrappers

Windows users do not need Git Bash for the helper scripts. The PowerShell runner also auto-installs the MCP checkout on first start. Use Windows paths in `~/.codex/config.toml` and override the MCP command to PowerShell if the GUI does not run the Bash wrapper:

```toml
[mcp_servers.ghostwriter]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\ghostwriter-mcp\\scripts\\run-ghostwriter-mcp.ps1"]

[mcp_servers.ghostwriter.env]
GHOSTWRITER_URL = "https://ghostwriter.example.com/"
GHOSTWRITER_API_KEY = "YOUR_API_KEY"
GHOSTWRITER_CA_BUNDLE = "C:\\path\\to\\ca-bundle.crt"
```

Optionally pre-warm or test the runner directly if the GUI does not show Ghostwriter tools:

```bash
~/.codex/plugins/ghostwriter-mcp/scripts/run-ghostwriter-mcp.sh
```

Set `GHOSTWRITER_MCP_AUTO_INSTALL=0` to disable first-run bootstrap. Expected Codex tool namespace: `mcp__ghostwriter__*`.

## Quick Setup

Use the `/ghostwriter-mcp:config` command to configure settings:

```
/ghostwriter-mcp:config --api-key "your_api_key"
/ghostwriter-mcp:config --url "https://ghostwriter.example.com/"
/ghostwriter-mcp:config --ca-bundle "/path/to/ca.crt"
```

Combine options: `/ghostwriter-mcp:config --api-key "key" --url "https://..."`

Get API key: Ghostwriter UI → Profile → API Tokens

## Configuration

Settings stored in `.claude/settings.local.json`:

```json
{
  "env": {
    "GHOSTWRITER_API_KEY": "your_api_key",
    "GHOSTWRITER_URL": "https://ghostwriter.example.com/",
    "GHOSTWRITER_CA_BUNDLE": "/path/to/ca.crt"
  }
}
```

**Defaults (pre-configured for SpecterOps internal):**
- `GHOSTWRITER_URL`: `https://gw.icp.specterops.io/`
- `GHOSTWRITER_CA_BUNDLE`: SpecterOps root CA (bundled)

## Available Tools (12)

**General**
- `whoami` - Verify API connection
- `graphql_health_check` - Check GraphQL endpoint

**Projects**
- `list_projects` - List projects with filtering
- `get_project` - Get project details by ID
- `search_clients` - Search clients by name

**Reporting**
- `generate_report` - Generate report document

**Findings**
- `list_project_findings` - List findings for a project
- `list_finding_library` - List finding library entries

**Oplog**
- `list_oplogs` - List operation logs
- `get_oplog` - Get oplog details with entries
- `create_oplog` - Create new operation log
- `create_oplog_entry` - Add entry to an oplog

## Usage

After installing plugin, use `/mcp` to verify connection. Tools available as `mcp__ghostwriter__*`.
