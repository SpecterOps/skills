# Reverse Engineering

Reverse engineering workflows and MCP-assisted binary analysis, starting with Binary Ninja.

## Skills

- `binary-ninja-mcp-analysis` — BNIL documentation, Binary Ninja analysis recipes, and BinjaMCP tool usage guidance.

## Purpose

This plugin is the Codex home for reverse-engineering workflows. It currently packages Binary Ninja MCP guidance and reference material, and is intended to hold future RE tooling skills.

## Prerequisites

- Binary Ninja with the BinjaMCP plugin or server installed.
- Codex MCP configuration for the Binary Ninja MCP command or endpoint when live tool use is needed.

## Codex Binary Ninja MCP setup

This plugin includes Binary Ninja MCP-aware skills and references, but it does not install, start, or wrap BinjaMCP. Configure the MCP server directly using the command or endpoint documented by your BinjaMCP installation.

For a stdio MCP server, add a direct Codex MCP entry to `~/.codex/config.toml` or project `.codex/config.toml`:

```toml
[mcp_servers.binary_ninja]
command = "/path/to/binja-mcp-server"
args = []
```

Restart Codex after editing MCP configuration and confirm the Binary Ninja MCP server is visible under `/mcp` before using live Binary Ninja workflows.
