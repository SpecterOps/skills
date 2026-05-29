---
name: ghidra-mcp-analysis
description: Use for reverse engineering and binary analysis with LaurieWired/GhidraMCP. Trigger for Ghidra MCP setup, bridge_mcp_ghidra.py usage, GhidraMCP plugin workflows, decompilation, function/string/import/export/xref analysis, renaming functions/data/variables, setting comments/types/prototypes, or producing Ghidra-backed RE notes.
metadata:
  author: "GhostWorks"
---

# Ghidra MCP Analysis

## Implementation target

This skill assumes the Ghidra MCP implementation is **LaurieWired/GhidraMCP**. It uses:

- a Ghidra extension/plugin that exposes a local HTTP server from Ghidra, defaulting to `http://127.0.0.1:8080/`
- `bridge_mcp_ghidra.py`, a Python MCP bridge that talks to the Ghidra-side HTTP server
- stdio transport by default for Codex MCP, with optional SSE mode for clients that need it

## Setup checklist

1. Install Ghidra and Python 3.
2. Download a LaurieWired/GhidraMCP release ZIP.
3. In Ghidra: `File` -> `Install Extensions` -> `+` -> select the `GhidraMCP-*.zip` release.
4. Restart Ghidra.
5. Enable `GhidraMCPPlugin` in `File` -> `Configure` -> `Developer`.
6. Optionally configure the Ghidra-side HTTP port with `Edit` -> `Tool Options` -> `GhidraMCP HTTP Server`.
7. Configure Codex to run the bridge:

```toml
[mcp_servers.ghidra]
command = "python3"
args = [
  "/ABSOLUTE_PATH_TO/GhidraMCP/bridge_mcp_ghidra.py",
  "--ghidra-server",
  "http://127.0.0.1:8080/"
]
```

Restart Codex and verify the `ghidra` MCP server is visible under `/mcp` before using live analysis.

## Available LaurieWired/GhidraMCP capabilities

Use these capabilities by their MCP tool names when available:

| Capability | Tool(s) |
|---|---|
| Current context | `get_current_address`, `get_current_function`, `get_function_by_address` |
| Function listing/search | `list_methods`, `list_functions`, `search_functions_by_name` |
| Classes/namespaces | `list_classes`, `list_namespaces` |
| Decompilation/disassembly | `decompile_function`, `decompile_function_by_address`, `disassemble_function` |
| Imports/exports/segments/data | `list_imports`, `list_exports`, `list_segments`, `list_data_items` |
| Strings | `list_strings` with optional `filter` |
| Xrefs | `get_xrefs_to`, `get_xrefs_from`, `get_function_xrefs` |
| Renaming | `rename_function`, `rename_function_by_address`, `rename_data`, `rename_variable` |
| Comments | `set_decompiler_comment`, `set_disassembly_comment` |
| Types/prototypes | `set_function_prototype`, `set_local_variable_type` |

## Recommended workflow

1. **Orient**
   - Confirm Ghidra has the target program open and analyzed.
   - Use `get_current_function` / `get_current_address` when the user points at something in the UI.
   - Use `list_segments`, `list_imports`, `list_exports`, and filtered `list_strings` for initial context.

2. **Survey efficiently**
   - Prefer `search_functions_by_name` and `list_strings(filter=...)` over dumping everything.
   - Use pagination (`offset`, `limit`) for `list_methods`, `list_classes`, `list_imports`, `list_exports`, `list_data_items`, and `list_strings`.

3. **Analyze functions**
   - Use `decompile_function_by_address` when an address is known.
   - Use `decompile_function` when a stable symbol/function name is known.
   - Use `disassemble_function` when decompiler output is ambiguous, optimized out, or missing low-level details.

4. **Trace relationships**
   - Use `get_xrefs_to` / `get_xrefs_from` for address-oriented tracing.
   - Use `get_function_xrefs` for function-name-oriented tracing.
   - Build source -> transform -> sink chains with exact addresses and function names.

5. **Annotate only with evidence**
   - Use `rename_function_by_address` or `rename_function` when behavior is confirmed.
   - Use `rename_variable`, `rename_data`, `set_function_prototype`, and `set_local_variable_type` incrementally.
   - Use `set_decompiler_comment` or `set_disassembly_comment` to record reasoning at important addresses.

6. **Report**
   - Include addresses, original names, new names/comments/types applied, decompiler/disassembly evidence, xref paths, and confidence.
   - Separate confirmed behavior from hypotheses.

## Reference loading

Read `references/workflow.md` for LaurieWired/GhidraMCP transport details, tool recipes, and output templates.
