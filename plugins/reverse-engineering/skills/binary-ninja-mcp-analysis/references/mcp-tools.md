# MCP Tools Reference

Complete reference for all BinjaMCP server tools. All address parameters accept hex strings (e.g., `'0x1000'`). Most tools accept an optional `file_path` parameter; when omitted, the most recently loaded binary is used.

## Binary Lifecycle

### `load_binary`
Load a binary file into Binary Ninja for analysis.
- `file_path: str` -- Absolute path to the binary file
- Returns: Summary (arch, platform, entry point, function count, segments)

### `list_loaded_binaries`
List all currently loaded binaries.
- No parameters
- Returns: List of loaded file paths

### `close_binary`
Close a binary and free resources.
- `file_path: str` -- Path of the binary to close

## Function Discovery

### `list_functions`
List functions in the binary (paginated).
- `offset: int = 0` -- Starting index
- `limit: int = 100` -- Max results
- Returns: Table of address, name, size

### `search_functions`
Search functions by name (case-insensitive substring).
- `query: str` -- Search string
- Returns: Up to 100 matching functions with address and name

### `get_function_info`
Detailed metadata about a function.
- `address: str` -- Hex address of function
- Returns: Name, address range, size, basic block count, is_exported, is_thunk, type, comment, callers, callees

### `get_function_type`
Get the full type signature of a function (return type, parameters, calling convention).
- `address: str` -- Hex address of function
- Returns: Function prototype string and detailed parameter info

## IL & Decompilation

### `decompile_function`
Decompile to pseudo-C using HLIL.
- `address: str` -- Hex address of function
- Returns: Pseudo-C decompilation (falls back to HLIL text)

### `get_hlil`
Get High Level IL representation.
- `address: str` -- Hex address
- Returns: HLIL text (address: instruction per line)

### `get_mlil`
Get Medium Level IL representation.
- `address: str` -- Hex address
- Returns: MLIL text (address: instruction per line)

### `get_llil`
Get Low Level IL representation.
- `address: str` -- Hex address
- Returns: LLIL text (address: instruction per line)

### `get_disassembly`
Get native disassembly.
- `address: str` -- Hex start address
- `length: int = 64` -- Bytes to disassemble (if inside a function, disassembles full function)
- Returns: Disassembly lines with addresses

## Strings

### `list_strings`
List strings in the binary (paginated).
- `offset: int = 0` -- Starting index
- `limit: int = 100` -- Max results
- `min_length: int = 4` -- Minimum string length
- Returns: Table of address, type, value

### `search_strings`
Search strings by content (case-insensitive substring).
- `query: str` -- Search string
- Returns: Matching strings with address and value

## Cross-References & Call Graph

### `get_xrefs_to`
Get references TO an address (who references this).
- `address: str` -- Target hex address
- Returns: Code and data references pointing to this address

### `get_xrefs_from`
Get references FROM an address (what this references).
- `address: str` -- Source hex address
- Returns: Addresses referenced from this location

### `get_function_callers`
Get functions that call a given function.
- `address: str` -- Hex address of the target function
- Returns: List of calling functions with address and name

### `get_function_callees`
Get functions called by a given function.
- `address: str` -- Hex address of the calling function
- Returns: List of called functions with address and name

## Imports & Exports

### `list_imports`
List all imported symbols.
- Returns: Table of address, type, name

### `search_imports`
Search imported symbols by name (case-insensitive substring).
- `query: str` -- Search string
- Returns: Matching imports with address and name

### `list_exports`
List all exported symbols.
- Returns: Table of address, name

## Binary Structure

### `list_sections`
List sections in the binary.
- Returns: Table of name, address range, size, semantics

### `list_segments`
List memory segments.
- Returns: Table of address range, size, rwx permissions

## Variables & Data

### `list_variables`
List local variables for a function.
- `address: str` -- Hex address of the function
- Returns: Table of variable name, type, source_type, storage

### `list_data_variables`
List global data variables in the binary (paginated).
- `offset: int = 0` -- Starting index
- `limit: int = 100` -- Max results
- Returns: Table of address, type, name/symbol

### `get_data_var_at`
Get type and value information for a data variable at a specific address.
- `address: str` -- Hex address
- Returns: Type, value, and symbol information

### `get_basic_blocks`
List basic blocks for a function.
- `address: str` -- Hex address of the function
- Returns: Table of block start, end, size, and outgoing edge targets

## Annotation

### `rename_function`
Rename a function.
- `address: str` -- Hex address of function
- `new_name: str` -- New name
- Returns: Confirmation with old and new names

### `rename_variable`
Rename a local variable within a function.
- `function_address: str` -- Hex address of the containing function
- `old_name: str` -- Current variable name
- `new_name: str` -- New variable name
- Returns: Confirmation message

### `set_comment`
Set a comment at an address.
- `address: str` -- Hex address
- `comment: str` -- Comment text (empty string to remove)

### `set_function_comment`
Set a comment on a function.
- `address: str` -- Hex address of function
- `comment: str` -- Comment text (empty string to remove)

### `set_function_type`
Set or change a function's type signature.
- `address: str` -- Hex address of function
- `type_string: str` -- C-style function type (e.g., `"int foo(char* buf, int len)"`)
- Returns: Confirmation with old and new type

## Raw Data

### `read_bytes`
Read raw bytes from the binary.
- `address: str` -- Hex address
- `length: int = 64` -- Bytes to read (max 4096)
- Returns: Hex dump with hex + ASCII columns

## Usage Tips

- **Start broad, narrow down**: Use `search_*` tools before `list_*` to avoid large outputs
- **HLIL first**: `decompile_function` gives the most readable output; drop to MLIL/LLIL when precision matters
- **Paginate large results**: `list_functions` and `list_strings` support `offset`/`limit`
- **Function lookup is fuzzy**: Most tools accepting a function address will also work with addresses *inside* the function (falls back to `get_functions_containing`)
- **Annotate as you go**: Use `rename_function`, `rename_variable`, and `set_comment` to build understanding incrementally
