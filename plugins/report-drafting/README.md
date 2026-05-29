# Report Drafting

Finding, report drafting, Ghostwriter MCP, and operation log workflows for security assessment deliverables.

## Skills

- `finding-report` — evidence-backed vulnerability finding drafts and remediation guidance.
- `ghostwriter-mcp` — Ghostwriter MCP setup, connection verification, project discovery, and oplog discovery.
- `ghostwriter-oplog` — quick, evidence-backed, guided, and configuration-oriented Ghostwriter operation log entries.

## Codex Ghostwriter MCP setup

This plugin includes Ghostwriter MCP-aware skills, but it does not install, clone, update, or run the external Ghostwriter MCP server for you. Follow Codex MCP configuration directly: install or clone the server yourself, then point Codex at that checkout.

Install the external server using its upstream instructions. A typical checkout uses:

```bash
git clone https://github.com/SpecterOps/GhostWriterMCP.git /path/to/GhostWriterMCP
cd /path/to/GhostWriterMCP
uv sync
```

Then add the MCP server to `~/.codex/config.toml` or project `.codex/config.toml`:

```toml
[mcp_servers.ghostwriter]
command = "uv"
args = ["--directory", "/path/to/GhostWriterMCP", "run", "python", "-m", "ghostwritermcp.server"]

[mcp_servers.ghostwriter.env]
GHOSTWRITER_URL = "https://ghostwriter.example.com/"
GHOSTWRITER_API_KEY = "YOUR_API_KEY"
GHOSTWRITER_CA_BUNDLE = "/path/to/ca-bundle.crt"
GHOSTWRITER_OPLOG_ID = "123"
GHOSTWRITER_OPERATOR = "your-callsign"
GHOSTWRITER_SOURCE_IP = "10.0.0.5"
```

Restart Codex after editing MCP configuration and confirm the `ghostwriter` server is visible under `/mcp` before using Ghostwriter workflows. Do not commit environment-specific API values.

## Agents

- `report-writer`
