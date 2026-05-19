# Binary Ninja MCP Skill (`binary-ninja-mcp`)

A skill plugin for Claude Code that provides Binary Ninja IL documentation and MCP server usage guidance for binary analysis and reverse engineering.

## Purpose

This plugin provides a comprehensive skill (`binary-ninja-mcp-analysis`) that gives Claude Code deep knowledge of:

- **BNIL (Binary Ninja Intermediate Language)** -- the family of ILs (LLIL, MLIL, HLIL) with complete instruction references
- **BinjaMCP server tools** -- documentation for all MCP tools exposed by the Binary Ninja MCP server
- **Analysis patterns** -- common workflows, recipes, and best practices for reverse engineering with Binary Ninja
- **Annotation** -- how to apply types, rename functions/variables, set comments, and define structures

## Prerequisites

- Binary Ninja with the [BinjaMCP](https://github.com/xpn/binary-ninja-mcp) plugin installed and running
- Claude Code MCP client configured to connect to `http://127.0.0.1:8080/mcp` (streamable-http transport)

## Skill Contents

| Reference Document | Description |
|-------------------|-------------|
| `bnil-overview.md` | IL hierarchy, reading notation, visitor/traverse APIs |
| `bnil-llil.md` | Low Level IL instruction reference |
| `bnil-mlil.md` | Medium Level IL instruction reference + Variable/Type system |
| `bnil-hlil.md` | High Level IL instruction reference (decompiler output) |
| `concepts.md` | BinaryView, IL walking, SSA, mapping between ILs |
| `cookbook.md` | Common analysis recipes and code patterns |
| `annotations.md` | Symbols, types, tags, and type application |
| `mcp-tools.md` | Complete BinjaMCP tool reference with parameters |

## Usage

The skill is automatically loaded when Claude Code detects binary analysis tasks. You can also manually invoke it:

```
/binary-ninja-mcp:binary-ninja-mcp-analysis
```

## Environment

No environment variables required. The MCP server runs within Binary Ninja and is accessed over HTTP.
