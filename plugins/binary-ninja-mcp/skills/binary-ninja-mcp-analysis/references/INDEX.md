# Reference Index

Master index of all Binary Ninja analysis reference documents.

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [BNIL Overview](./bnil-overview.md) | IL family hierarchy, reading notation (size specifiers, comparisons, macros), visitor APIs | When you need to understand IL output notation or decide which IL level to use |
| [LLIL Reference](./bnil-llil.md) | Complete Low Level IL instruction set grouped by category | When reading `get_llil` output or analyzing register/flag-level operations |
| [MLIL Reference](./bnil-mlil.md) | Complete Medium Level IL instruction set, Variable and Type object documentation | When reading `get_mlil` output or working with variables and types |
| [HLIL Reference](./bnil-hlil.md) | Complete High Level IL instruction set including control flow recovery | When reading `decompile_function` / `get_hlil` output |
| [Important Concepts](./concepts.md) | BinaryView, walking ILs, IL mapping, SSA, instruction vs expression index, analysis limits | When you need to understand core BN concepts or how ILs relate to each other |
| [Cookbook](./cookbook.md) | Common analysis recipes: navigation, IL access, call graphs, variables, xrefs, types | When you need patterns for common analysis tasks |
| [Annotations](./annotations.md) | Symbols, tags, types (creation and application), function signatures, data variables | When annotating binaries: renaming, typing, commenting |
| [MCP Tools Reference](./mcp-tools.md) | Complete reference for all BinjaMCP server tools with parameters and usage patterns | When you need to know what tools are available and how to call them |
