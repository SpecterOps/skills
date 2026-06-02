# Reverse Engineering

Reverse engineering workflows and MCP-assisted binary analysis for Binary Ninja, Ghidra, and related tooling.

## Skills

- `binary-ninja-mcp-analysis` — BNIL documentation, Binary Ninja analysis recipes, and BinjaMCP tool usage guidance.
- `ghidra-mcp-analysis` — Ghidra MCP binary analysis workflow, capability mapping, and annotation guidance.

## Purpose

This plugin is the Codex home for reverse-engineering workflows. It packages MCP-assisted Binary Ninja and Ghidra guidance plus reference material for future RE tooling skills.

## Prerequisites

- Binary Ninja installed and licensed on the machine that will run analysis.
- The `fosdickio/binary_ninja_mcp` Binary Ninja plugin installed separately from this plugin.
- `npx` available on the PATH used by Codex when using the recommended bridge.
- Binary Ninja open with the target binary loaded before using live MCP tools.
- Ghidra with a Ghidra MCP server/plugin/bridge installed when using Ghidra workflows.
- Codex MCP configuration for the selected RE MCP command or endpoint when live tool use is needed.

## Codex Binary Ninja MCP setup

This plugin includes Binary Ninja MCP-aware skills and references, but it does not install, start, or wrap `fosdickio/binary_ninja_mcp`. Configure that MCP server directly in Codex.

The `fosdickio/binary_ninja_mcp` project has two parts:

- A Binary Ninja plugin that exposes Binary Ninja capabilities through a local MCP/HTTP service.
- A bridge command that MCP clients run to connect to that local Binary Ninja service.

### Install the Binary Ninja plugin

Install `fosdickio/binary_ninja_mcp` through Binary Ninja's Plugin Manager (`Plugins > Manage Plugins`) when available, or manually copy/clone the repository into Binary Ninja's plugins folder according to the upstream README.

After installation:

1. Open Binary Ninja.
2. Load the binary or BNDB you want Codex to analyze.
3. Start or enable the Binary Ninja MCP plugin from the Binary Ninja UI.
4. Confirm the plugin is listening on the expected host and port. The upstream default shown in its MCP client config is `localhost:9009`.

### Recommended Codex config

Add this direct MCP entry to `~/.codex/config.toml` or project `.codex/config.toml`:

```toml
[mcp_servers.binary_ninja_mcp]
command = "npx"
args = ["-y", "binary-ninja-mcp", "--host", "localhost", "--port", "9009"]
```

If your Binary Ninja plugin listens on a different host or port, update the `--host` and `--port` values to match.

### Legacy Python bridge

The upstream project also documents a Python bridge. Use this only when the npm bridge is not suitable for the environment:

```toml
[mcp_servers.binary_ninja_mcp]
command = "/ABSOLUTE/PATH/TO/binary_ninja_mcp/.venv/bin/python"
args = ["/ABSOLUTE/PATH/TO/binary_ninja_mcp/bridge/binja_mcp_bridge.py"]
```

Replace `/ABSOLUTE/PATH/TO/binary_ninja_mcp` with the actual plugin checkout path. The Python interpreter must be the virtualenv where the bridge dependencies are installed.

### Verification

After editing MCP configuration, restart Codex and run `/mcp`. Confirm the `binary_ninja_mcp` server appears before using `binary-ninja-mcp-analysis` for live work. Then verify with a low-risk tool call such as `get_binary_status`, `list_binaries`, `list_methods`, `list_strings`, or `list_imports` depending on the tool list exposed in your current install.

### Troubleshooting

- If Codex cannot start the bridge, confirm `npx` is available in the same environment Codex uses.
- If the bridge starts but cannot connect, confirm the Binary Ninja plugin is running and listening on the same host and port configured in Codex.
- If the MCP has no binary context, open a binary or BNDB in Binary Ninja and select it in the plugin/UI.
- If tool names differ from this plugin's references, trust the installed MCP server's live `/mcp` tool list and use this plugin's BNIL/reference material as conceptual guidance.

Upstream reference: https://github.com/fosdickio/binary_ninja_mcp

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
