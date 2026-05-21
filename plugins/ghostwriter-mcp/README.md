# Ghostwriter MCP Plugin

Claude Code plugin for Ghostwriter security documentation platform.

## Prerequisites

- [UV](https://docs.astral.sh/uv/) package manager
- Running Ghostwriter instance


## Codex GUI app setup

After installing `ghostwriter-mcp` from the Codex GUI `/plugins` view, install the MCP server dependency into the installed plugin copy. The installer requires a source because this repository does not bundle a canonical Ghostwriter MCP server checkout:

```bash
cd ~/.codex/plugins/ghostwriter-mcp
GHOSTWRITER_MCP_SOURCE='<git-url-or-local-path-to-ghostwriter-mcp-server>' \
  scripts/install-mcp-deps.sh
```

Add Ghostwriter connection values to `~/.codex/config.toml` so the GUI app can see them, then fully restart Codex:

```toml
[mcp_servers.ghostwriter.env]
GHOSTWRITER_MCP_DIR = "/home/matthew/.codex/plugins/ghostwriter-mcp/vendor/ghostwriter-mcp"
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

Windows users do not need Git Bash for the helper scripts. Install dependencies from PowerShell after the plugin is installed:

```powershell
cd $env:USERPROFILE\.codex\plugins\bloodhound-analysis
.\scripts\install-mcp-deps.ps1

cd $env:USERPROFILE\.codex\plugins\ghostwriter-mcp
.\scripts\install-mcp-deps.ps1 -Source '<git-url-or-local-path-to-ghostwriter-mcp-server>'
```

Use Windows paths in `~/.codex/config.toml` and override the MCP command to PowerShell if the GUI does not run the Bash wrappers:

```toml
[mcp_servers.bloodhound_mcp]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\bloodhound-analysis\\scripts\\run-bloodhound-mcp.ps1"]

[mcp_servers.bloodhound_mcp.env]
BLOODHOUND_MCP_DIR = "C:\\Users\\<you>\\.codex\\plugins\\bloodhound-analysis\\vendor\\bloodhound-mcp"

[mcp_servers.ghostwriter]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\ghostwriter-mcp\\scripts\\run-ghostwriter-mcp.ps1"]

[mcp_servers.ghostwriter.env]
GHOSTWRITER_MCP_DIR = "C:\\Users\\<you>\\.codex\\plugins\\ghostwriter-mcp\\vendor\\ghostwriter-mcp"
```

Test the runner directly if the GUI does not show Ghostwriter tools:

```bash
~/.codex/plugins/ghostwriter-mcp/scripts/run-ghostwriter-mcp.sh
```

Expected Codex tool namespace: `mcp__ghostwriter__*`.

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
