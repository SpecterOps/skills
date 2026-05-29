---
name: binary-ninja-mcp-analysis
description: Provides Binary Ninja IL documentation and MCP server usage guidance for binary analysis and reverse engineering
license: MIT
metadata:
  author: xpn
  version: "0.1.0"
  category: security
---

# Binary Ninja Analysis Skill

## When to Use

Use this skill when working with Binary Ninja via the BinjaMCP server to analyze binaries. This includes:

- Loading and analyzing binary files (ELF, PE, Mach-O, etc.)
- Decompiling functions and understanding decompiler output
- Reading or interpreting Binary Ninja Intermediate Language (BNIL) output at any level (LLIL, MLIL, HLIL)
- Reverse engineering functions, understanding control flow, or tracing data flow
- Annotating binaries (renaming functions/variables, setting comments, applying types)
- Searching for strings, imports, exports, or cross-references
- Understanding the structure of a binary (sections, segments, symbols)

## When NOT to Use

Do not use this skill when the task does not involve binary analysis or reverse engineering with Binary Ninja. If you are writing Binary Ninja plugins in Python (not using the MCP server), this skill's MCP tool reference may not apply but the BNIL documentation is still relevant.

You must never use this skill unless the MCP server is available and the task involves interacting with Binary Ninja's analysis capabilities. If the task is purely theoretical or does not involve Binary Ninja, this skill is not appropriate.

## Runtime Requirements

Codex should be configured directly with a `mcp_servers.binary_ninja` entry that runs the BinjaMCP command or endpoint documented by the user's BinjaMCP installation. This plugin does not install, start, or wrap the Binary Ninja MCP server. Verify the Binary Ninja MCP tools are visible under `/mcp` before using live analysis workflows.

## Terminology

- **BNIL** - Binary Ninja Intermediate Language. The family of ILs used by Binary Ninja.
- **LLIL** - Low Level IL. Closest to assembly; operates on registers, flags, and memory addresses.
- **MLIL** - Medium Level IL. Translates registers to variables, associates types, propagates constants.
- **HLIL** - High Level IL. Decompiler output with recovered control flow (if/while/for/switch).
- **SSA** - Static Single Assignment. IL form where each variable is written exactly once; versions track modifications.
- **BinaryView (bv)** - Top-level analysis object representing a loaded binary.
- **Function** - A function identified by Binary Ninja, accessed by its start address.
- **BasicBlock** - A straight-line sequence of instructions with one entry and one exit.
- **Cross-reference (xref)** - A reference from one address to another (code or data).

## MCP Server Overview

The BinjaMCP server exposes tools for interacting with Binary Ninja. Tools are grouped as:

| Category | Tools | Purpose |
|----------|-------|---------|
| Lifecycle | `load_binary`, `list_loaded_binaries`, `close_binary` | Load/manage binaries |
| Functions | `list_functions`, `search_functions`, `get_function_info`, `get_function_type` | Discover and inspect functions |
| IL / Decompilation | `decompile_function`, `get_hlil`, `get_mlil`, `get_llil`, `get_disassembly` | View code at different abstraction levels |
| Strings | `list_strings`, `search_strings` | Find string data |
| Cross-refs | `get_xrefs_to`, `get_xrefs_from`, `get_function_callers`, `get_function_callees` | Trace references and call graphs |
| Imports/Exports | `list_imports`, `search_imports`, `list_exports` | Inspect symbol tables |
| Structure | `list_sections`, `list_segments` | Understand binary layout |
| Annotation | `rename_function`, `rename_variable`, `set_comment`, `set_function_comment`, `set_function_type` | Annotate the binary |
| Variables/Data | `list_variables`, `list_data_variables`, `get_data_var_at`, `get_basic_blocks` | Inspect variables, globals, CFG |
| Raw Data | `read_bytes` | Read raw memory |

## Choosing an IL Level

- **HLIL** (`decompile_function` / `get_hlil`): Best for initial understanding. Recovers if/while/for/switch. Use for vulnerability analysis, logic review, and getting a high-level picture. Note: tree-based, so nested expressions can hide instructions.
- **MLIL** (`get_mlil`): Best for precise analysis. Variables have types, constants are propagated, call parameters are resolved. Less folding than HLIL so easier to iterate linearly. Preferred for data flow tracing.
- **LLIL** (`get_llil`): Best for low-level analysis. Shows register/flag operations, stack manipulation. Use when you need to understand exact instruction semantics or flag behavior.
- **Disassembly** (`get_disassembly`): Raw native instructions. Use when IL abstractions lose important detail (e.g., specific instruction encodings, alignment).

## Recommended Analysis Workflow

1. **Load**: `load_binary` to open the target
2. **Survey**: `list_functions` + `list_imports` + `list_strings` to understand scope
3. **Target**: `search_functions` or `search_strings` to find areas of interest
4. **Analyze**: `decompile_function` for initial understanding, then `get_mlil` or `get_llil` for precision
5. **Trace**: `get_xrefs_to` / `get_function_callers` to understand how a function is reached
6. **Annotate**: `rename_function`, `rename_variable`, `set_comment` to document findings
7. **Iterate**: Use cross-references and call graphs to follow the analysis deeper

## Context Efficiency Tips

- Use `search_functions` / `search_strings` / `search_imports` instead of listing everything
- Start with `decompile_function` (HLIL pseudo-C) before falling back to lower ILs
- Use `get_function_info` to get metadata (size, callers, callees) before reading full IL
- Use pagination (`offset`/`limit`) on `list_functions` and `list_strings` for large binaries
- Prefer `get_function_callers`/`get_function_callees` over raw xref queries for call graph analysis

## References

For detailed information on specific areas, consult the [Reference Index](./references/INDEX.md).

Key references:

* [Reference Index](./references/INDEX.md) - Master index of all documentation
* [BNIL Overview](./references/bnil-overview.md) - IL family overview, notation, and reading guide
* [LLIL Reference](./references/bnil-llil.md) - Low Level IL instruction set
* [MLIL Reference](./references/bnil-mlil.md) - Medium Level IL instruction set, variables, and types
* [HLIL Reference](./references/bnil-hlil.md) - High Level IL instruction set with control flow recovery
* [Important Concepts](./references/concepts.md) - BinaryView, IL walking, SSA, mapping between ILs
* [Cookbook](./references/cookbook.md) - Common analysis recipes and patterns
* [Annotations](./references/annotations.md) - Symbols, types, tags, and type application
* [MCP Tools Reference](./references/mcp-tools.md) - Complete reference for all BinjaMCP server tools
