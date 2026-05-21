# ghostwriter-oplog

Quick logging commands for GhostWriter operation logs during security assessments.

## Prerequisites

- GhostWriter MCP server configured and running (provides `create_oplog_entry` tool)
- Active oplog in GhostWriter


## Codex GUI app setup

Install both `ghostwriter-mcp` and `ghostwriter-oplog` from the Codex GUI `/plugins` view. `ghostwriter-oplog` depends on the Ghostwriter MCP tools provided by `ghostwriter-mcp`; complete the `ghostwriter-mcp` Codex GUI setup first.

Set oplog defaults in the GUI-visible Ghostwriter MCP env block in `~/.codex/config.toml`, then fully restart Codex:

```toml
[mcp_servers.ghostwriter.env]
GHOSTWRITER_OPLOG_ID = "123"
GHOSTWRITER_OPERATOR = "your-callsign"
GHOSTWRITER_SOURCE_IP = "10.0.0.5"
```


On Windows, complete the `ghostwriter-mcp` PowerShell wrapper setup first if the Codex GUI cannot launch Bash-based MCP runners. The oplog skill only needs the `mcp__ghostwriter__*` tools and the oplog env values.

Legacy aliases are still accepted by the skill if already present: `GW_OPLOG_ID`, `GW_OPERATOR_NAME`, and `GW_SOURCE_IP`.

In the Codex GUI, use the `ghostwriter-oplog` skill for `quick`, `evidence`, `guided`, or `config` workflows after the `mcp__ghostwriter__*` tools are available.

## Setup

Use `/ghostwriter-oplog:config` to configure settings:

```
/ghostwriter-oplog:config --oplog-id 123 --operator "your-callsign"
/ghostwriter-oplog:config --source-ip "10.0.0.5"
```

Combine options: `/ghostwriter-oplog:config --oplog-id 123 --operator "callsign" --source-ip "10.0.0.5"`

Settings stored in `.claude/settings.local.json`:

```json
{
  "env": {
    "GW_OPLOG_ID": "123",
    "GW_OPERATOR_NAME": "your-callsign",
    "GW_SOURCE_IP": "10.0.0.5"
  }
}
```

## Commands

### `/ghostwriter-oplog:quick <description>`

Quick timestamped log entry for key events.

```
/ghostwriter-oplog:quick Gained initial access via phishing payload
/ghostwriter-oplog:quick --tags creds,objective:1 Found domain admin hash in LSASS
```

### `/ghostwriter-oplog:evidence <file> <description>`

Log entry with file contents as evidence.

```
/ghostwriter-oplog:evidence /tmp/hashes.txt Dumped NTDS hashes from DC01
/ghostwriter-oplog:evidence ./screenshot.png --tags vuln Evidence of SQLi in login form
```

### `/ghostwriter-oplog:guided`

Interactive walkthrough for detailed entries. Prompts for:
- Entry type (command, discovery, creds, evidence)
- Description
- Evidence file (optional)
- Destination IP/target
- Tool used
- Tags (multi-select)

Use when you want to fill in all oplog fields without remembering the syntax.

## Tags

GhostWriter displays tags with special styling:
- `att&ck`, `attack`, `mitre`, `ttp` - red (e.g., `ttp:t1003`)
- `creds`, `credentials` - yellow
- `vuln` - green
- `detect` - blue
- `objective` - purple (e.g., `objective:1`)
