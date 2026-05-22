# Report Writing

Finding, report drafting, Ghostwriter MCP, and operation log workflows for security assessment deliverables.

## Skills

- `finding-report` — evidence-backed vulnerability finding drafts and remediation guidance.
- `ghostwriter-mcp` — Ghostwriter MCP setup, connection verification, project discovery, and oplog discovery.
- `ghostwriter-oplog` — quick, evidence-backed, guided, and configuration-oriented Ghostwriter operation log entries.

## Codex GUI Ghostwriter MCP setup

Installing `report-writing` from the Codex GUI installs the Ghostwriter MCP config, skills, and helper scripts. The plugin-owned MCP runner clones/syncs `https://github.com/SpecterOps/GhostWriterMCP.git` into `vendor/ghostwriter-mcp` on first start.

Add Ghostwriter connection values to `~/.codex/config.toml`, then fully restart Codex:

```toml
[mcp_servers.ghostwriter.env]
GHOSTWRITER_URL = "https://ghostwriter.example.com/"
GHOSTWRITER_API_KEY = "YOUR_API_KEY"
GHOSTWRITER_CA_BUNDLE = "/path/to/ca-bundle.crt"
GHOSTWRITER_OPLOG_ID = "123"
GHOSTWRITER_OPERATOR = "your-callsign"
GHOSTWRITER_SOURCE_IP = "10.0.0.5"
```

Windows users can override the MCP command to PowerShell if the GUI does not run Bash wrappers:

```toml
[mcp_servers.ghostwriter]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\<you>\\.codex\\plugins\\report-writing\\scripts\\run-ghostwriter-mcp.ps1"]
```

Optional pre-warm:

```bash
~/.codex/plugins/report-writing/scripts/run-ghostwriter-mcp.sh
```

## Agents

- `report-writer`
