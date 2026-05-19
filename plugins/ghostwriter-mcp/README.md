# Ghostwriter MCP Plugin

Claude Code plugin for Ghostwriter security documentation platform.

## Prerequisites

- [UV](https://docs.astral.sh/uv/) package manager
- Running Ghostwriter instance

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
