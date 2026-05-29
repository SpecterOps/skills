# Reverse Engineering

Reverse engineering workflows and MCP-assisted binary analysis for Binary Ninja, Ghidra, and related tooling.

## Skills

- `binary-ninja-mcp-analysis` — BNIL documentation, Binary Ninja analysis recipes, and BinjaMCP tool usage guidance.
- `ghidra-mcp-analysis` — Ghidra MCP binary analysis workflow, capability mapping, and annotation guidance.

## Purpose

This plugin is the Codex home for reverse-engineering workflows. It packages MCP-assisted Binary Ninja and Ghidra guidance plus reference material for future RE tooling skills.

## Prerequisites

- Binary Ninja with the BinjaMCP plugin or server installed when using Binary Ninja workflows.
- Ghidra with a Ghidra MCP server/plugin/bridge installed when using Ghidra workflows.
- Codex MCP configuration for the selected RE MCP command or endpoint when live tool use is needed.

## Codex Binary Ninja MCP setup

This plugin includes Binary Ninja MCP-aware skills and references, but it does not install, start, or wrap BinjaMCP. Configure the MCP server directly using the command or endpoint documented by your BinjaMCP installation.

For a stdio MCP server, add a direct Codex MCP entry to `~/.codex/config.toml` or project `.codex/config.toml`:

```toml
[mcp_servers.binary_ninja]
command = "/path/to/binja-mcp-server"
args = []
```

Restart Codex after editing MCP configuration and confirm the Binary Ninja MCP server is visible under `/mcp` before using live Binary Ninja workflows.


## Codex Ghidra MCP setup

This plugin targets LaurieWired/GhidraMCP for Ghidra-backed MCP analysis. Install the Ghidra extension from a LaurieWired/GhidraMCP release, enable `GhidraMCPPlugin` in Ghidra, and point Codex at `bridge_mcp_ghidra.py`.

```toml
[mcp_servers.ghidra]
command = "python3"
args = [
  "/ABSOLUTE_PATH_TO/GhidraMCP/bridge_mcp_ghidra.py",
  "--ghidra-server",
  "http://127.0.0.1:8080/"
]
```

GhidraMCP defaults to the Ghidra-side server at `http://127.0.0.1:8080/`; change the URL if you configured a different host or port in Ghidra. Restart Codex after editing MCP configuration and confirm the Ghidra MCP server is visible under `/mcp` before using live Ghidra workflows.
