# LaurieWired/GhidraMCP Workflow Reference

## Architecture

LaurieWired/GhidraMCP has two parts:

1. **Ghidra plugin/extension**: runs inside Ghidra and exposes an HTTP server, default `http://127.0.0.1:8080/`.
2. **Python MCP bridge**: `bridge_mcp_ghidra.py`, which exposes MCP tools and forwards requests to the Ghidra HTTP server.

Default Codex stdio configuration:

```toml
[mcp_servers.ghidra]
command = "python3"
args = [
  "/ABSOLUTE_PATH_TO/GhidraMCP/bridge_mcp_ghidra.py",
  "--ghidra-server",
  "http://127.0.0.1:8080/"
]
```

Optional SSE bridge mode, useful for clients that consume remote MCP/SSE endpoints:

```bash
python3 bridge_mcp_ghidra.py   --transport sse   --mcp-host 127.0.0.1   --mcp-port 8081   --ghidra-server http://127.0.0.1:8080/
```

## Tool recipes

### UI-selected function triage

1. `get_current_function`
2. `get_current_address`
3. `decompile_function_by_address(<current address>)`
4. `get_xrefs_to(<current address>)`
5. `disassemble_function(<current address>)` if decompilation is unclear

### String-to-code workflow

1. `list_strings(filter="keyword")`
2. Pick string address.
3. `get_xrefs_to(<string address>)`
4. `get_function_by_address(<xref address>)`
5. `decompile_function_by_address(<function address>)`
6. Rename/comment once behavior is confirmed.

### Import-to-sink workflow

1. `list_imports(offset=0, limit=...)`
2. Identify suspicious API/import.
3. `get_xrefs_to(<import thunk/address>)` when an address is available.
4. Decompile caller functions and trace argument sources.
5. Use comments to mark source/validation/sink boundaries.

### Function search workflow

1. `search_functions_by_name("query")`
2. `decompile_function("matched_name")`
3. `get_function_xrefs("matched_name")`
4. Rename by address if the original symbol is unstable or duplicated.

## Annotation guidance

- Prefer address-based mutation tools when possible: `rename_function_by_address`, `set_function_prototype`, `set_local_variable_type`.
- Use `rename_function` only when the old name is unique and stable.
- Add a comment before or with a rename when the behavior is non-obvious.
- For type changes, record the evidence: call signature, field offset pattern, imported API contract, or observed constants.

## Output template

```markdown
## GhidraMCP Analysis Notes

Target: <program/binary>
Ghidra server: <host:port>
Objective: <question>

### Findings
- `<function/address>`: <confirmed behavior and evidence>

### Evidence table
| Address | Function | Evidence | Action taken | Confidence |
|---|---|---|---|---|

### Annotations applied
- `<address>`: renamed/commented/typed as `<value>` because <reason>

### Open questions
- <unknowns>

### Next steps
- <focused follow-up>
```
