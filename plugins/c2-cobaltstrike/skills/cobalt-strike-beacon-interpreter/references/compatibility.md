# Beacon Interpreter Script Compatibility Skills (Guide for AI Agents)

## Purpose
This document is a compatibility guide for generating C scripts that run correctly in the Cobalt Strike Interpreter VM.

It is written for AI agents that must produce scripts compatible with this implementation, with emphasis on:
- script compiler behavior
- VM/runtime behavior
- provided script headers in `interpreter-includes/`
- user-facing execution paths in Cobalt Strike

---

## 1) Target Runtime and Entry Paths

These scripts are designed to run with the Cobalt Strike Interpreter through one of these interfaces:
- Beacon console command: `beacon-interpreter`
- Aggressor Script function: `bbeacon_interpreter`
- Cobalt Strike client Script Editor Window 

---

## 2) Script Execution Model

1. There is no required implicit `main()` entrypoint.
2. Top-level statements act as script entry logic.
3. Function bodies execute only when called.
4. If you define `main()`, call it explicitly at top level (`main();`) when intended.

Runtime-provided globals:
- `__argc`
- `__argv`

These are ABI-provided globals populated by the runtime before execution.

---

## 3) Regular C vs Scripted C (What Changes and What Does Not)

Treat script authoring as regular C in most day-to-day coding:
- same core control flow (`if/else`, `for`, `while`, `switch`, `goto`)
- same core integer/pointer/array semantics
- same practical use of structs, enums, unions, typedefs, macros, and function calls
- same decomposition patterns (helpers, recursion, forward declarations)

The `interpreter_demo.c` script demonstrates this “normal C first” model with:
- macros and expressions
- recursion and helper functions
- struct/enum/union usage
- arrays and pointer arithmetic
- function pointers and native API calls

Where this implementation diverges from regular C, follow these rules:
- no `float` or `double`; use integer/fixed-point logic instead
- entry is top-level script statements, not an implicit `main()`
- `__argc` and `__argv` are Beacon packed-argument data, not POSIX `argc/argv`
- native API usage is through interpreter FFI signatures and provided headers
- `void *` must be cast before dereference/indexing
- struct/union by-value parameter/return forms are restricted; prefer pointer-based APIs
- some complex declarator shapes are intentionally restricted; keep declarations conservative
- macro support is practical but not equivalent to a full traditional C preprocessor
- runtime resource limits exist (stack/call depth/locals/globals); avoid unbounded designs

Practical guidance for AI agents:
- write scripts like normal C unless a known interpreter rule says otherwise
- when in doubt, prefer simpler declaration/call shapes that mirror proven patterns
- check provided headers before creating your own definitions

---

## 4) Argument Passing Model (Critical)

### 4.1 This is NOT normal C `argc/argv`
`__argc` and `__argv` are not POSIX-style argument count and `char **argv`.

In this VM:
- `__argc` is the size (in bytes) of a packed Beacon argument buffer.
- `__argv` is a pointer to that packed buffer.

Use Beacon APIs (`BeaconDataParse`, `BeaconDataExtract`, etc.) to read arguments, exactly like BOF argument parsing.

### 4.2 How arguments are passed from Cobalt Strike

#### Beacon console: `beacon-interpreter`
The user-facing help specifies:
- `beacon-interpreter [/path/to/script.c] [args]`
- args follow BOF packing syntax (`[format] [arg1] [arg2] ...`)
- example in help text: `z "Hello world"`

Meaning: console arguments are packed into a Beacon argument buffer before script execution.

#### Aggressor function: `bbeacon_interpreter`
`bbeacon_interpreter` passes the provided argument blob directly.

For compatibility, generate/expect packed BOF-style bytes (typically with `bof_pack(...)`) before calling `bbeacon_interpreter` from an aggressor script.

#### Script editor (Cobalt Strike client)
The Script Editor has an `Arguments` panel that builds packed argument bytes from typed rows.
Supported row types include:
- `short`
- `int`
- `long`
- `str`
- `widestr`
- `binary`
- `binary from file`

These rows are packed into the same argument blob model consumed by `__argc`/`__argv`.

### 4.3 Example argument extraction pattern

```c
#include <beacon.h>

/*
* Beacon passes the total size of the argument data in __argc while
* __argv holds a pointer to the data that can be extracted by using
* the Beacon API, exactly like it is handled in BOFs. Arguments can
* be added for the script in the Arguments section of the script
* editor. This example expects that a string argument was packed.
*/
if (__argc > 0) {
    datap args = {0};
    BeaconDataParse(&args, __argv, __argc);

    {
        char *message = BeaconDataExtract(&args, NULL);
        if (message != NULL) {
            BeaconPrintf(CALLBACK_OUTPUT, "Got message: %s", message);
        }
        else {
            BeaconPrintf(CALLBACK_ERROR, "Unknown message");
        }
    }
}
else {
    BeaconPrintf(CALLBACK_ERROR, "No arguments provided to script");
}
```

---

## 5) Include and Header Surface

Use only the provided interpreter headers via angle includes, for example:

```c
#include <windows.h>
#include <beacon.h>
```

Team Server include-resolution note:
- Do not use local/absolute/relative header paths in script includes.
- Use header names only (for example, `#include <windows.h>`).
- Includes are resolved by the Cobalt Strike Team Server when it compiles the script, against the interpreter header set available there.
- In practice, this means include targets are Team Server-relative, not relative to your local script directory.

### Preprocessor defines before includes
- Define platform/encoding selection macros at the very top of the script, before any `#include`, so they propagate into included headers.
- Default scripted-C behavior is effectively `_WIN64` selection, and ANSI variants are chosen when headers provide ANSI vs Unicode aliases.
- For 32-bit VM-targeted scripts, explicitly set:

```c
#define _WIN32
```

before any includes so 32-bit compatible header aliases/types are selected (for example, `IMAGE_NT_HEADERS` resolving to `IMAGE_NT_HEADERS32`).
- If you want Unicode-mapped APIs/types, explicitly set:

```c
#define UNICODE
```

before includes so Unicode equivalents are selected instead of ANSI forms.

`windows.h` pulls common Windows typedef/API coverage in this environment. `beacon.h` provides Beacon APIs such as:
- `BeaconDataParse`
- `BeaconDataExtract`
- `BeaconPrintf`
- `BeaconOutput`
- `BeaconFormat*` helpers

Important compatibility rule:
- Keep include paths and include names conservative and relative to the provided include set.
- Before defining your own structs, enums, typedefs, and FFI declarations, check provided headers first and reuse existing definitions.
- Only define your own Windows API structs/function signatures when they are not already present in the included headers.
- If you receive duplicate-definition errors, treat that as a signal that a definition already exists in one of your included headers and remove your duplicate.

### Large output guidance (Cobalt Strike client safety)
- When returning potentially large output, prefer the `BeaconFormat` API (`BeaconFormatAlloc`, `BeaconFormatPrintf`, `BeaconFormatToString`, `BeaconFormatFree`) to build output in a controlled buffer first.
- Allocate a buffer large enough for expected formatted data, then send results back in chunks instead of emitting one line/event at a time.
- Do not use `BeaconPrintf` in tight loops for high-volume output.
- Use `BeaconPrintf` sparingly for summary/status messages so client-side processing is not overwhelmed.
- For bulk data, format once, chunk, then emit each chunk through a controlled output path.

---

## 6) Language and Type Rules to Follow

### Supported core areas
- Integer scalar math (`char/short/int/long/long long`, signed and unsigned)
- Pointers, arrays, pointer arithmetic
- Struct/union/enum/typedef
- Control flow (`if/else`, loops, `switch`, `break`, `continue`, labels, `goto`)
- Functions, recursion, forward declarations
- Macro usage in practical script patterns
- Wide character and wide string workflows (`wchar_t`, `L"..."`, `L'X'`)

### Restrictions and pitfalls
- Do not rely on floating-point (`float`/`double`) support.
- Do not dereference/index `void *` directly; cast first.
- Script functions do not support var args (...) and cannot be called from function pointers
- Var args and function pointers are only supported in native ffi
- Keep declarators conservative; avoid exotic function-pointer forms.
- Be careful with wide/narrow literal mismatch in array initializers.

### Macro usage notes
- Macro usage is close to `#define` in regular C, but this is not a drop-in replacement for every traditional preprocessor pattern.
- Moderately complex macros are supported in practice, including parameterized macros, nested macro expansion, and expression macros with casts/dereferences.
- For best compatibility, keep macros expression-oriented and conservative.
- Do not target complex multi-line or statement-heavy macros; these are not supported as a compatibility baseline.
- When macro logic becomes complex, prefer a normal helper function instead.

---

## 7) Native FFI Contract

### Signature declaration form
Required style follows BOF DFR syntax of LIB$Function:

```c
KERNEL32$GetLastError: u32 ();
MSVCRT$printf: cdecl i32 (cstr, ...);
```

### Calling convention rules
- `cdecl`, `stdcall`, or omitted convention are accepted. Ommitted implies stdcall.
- `stdcall` with varargs is invalid. Varargs are only supported with `cdecl`.
- Specifying calling convention is unnecessary with 64-bit scripts. It is required when you want to run a script in a 32-bit Beacon VM. Failing to specify the correct calling convention in a 32-bit Beacon VM will result in a crash.

### Allowed FFI signature atom types
- `void`
- `i16`, `u16`
- `i32`, `u32`
- `i64`, `u64`
- `ptr`
- `cstr`
- `size_t`

### Argument matching behavior
- Non-varargs calls must match declared argument count.
- Pointer formals should receive pointer expressions (or null).
- The size_t atom type aligns with the SIZE_T windows api type and is always pointer-sized.
- The cstr atom type should be preferred when an string argument is expected but is technically equivalent with ptr.

### Bare name call behavior
If a matching declaration exists, bare calls like `printf(...)` will resolve and should be preferred.
If names are ambiguous across native declarations, use explicit `LIB$Func` naming.

---

## 8) Structural Compatibility Rules

1. Struct-to-struct assignment is valid for matching struct types.
2. Struct value assignment to scalar/pointer destinations is invalid.
3. Keep function parameter count conservative (implementation has fixed limits).
4. Prefer pointer-passing for complex aggregates.
5. Keep array declarations/initializers simple and type-consistent.

---

## 9) Layout Helpers

Use compiler-provided layout helpers for robust structure math:
- `__builtin_offsetof(...)`
- `CONTAINING_RECORD(...)` (from provided headers)

These are preferred over hardcoded offsets.

Example:

```c
#include <windows.h>
#include <beacon.h>

typedef struct _ITEM {
    int value;
} ITEM;

typedef struct _ITEM_WRAPPER {
    int tag;
    ITEM item;
} ITEM_WRAPPER;

void demo_layout_helpers(void)
{
    ITEM_WRAPPER wrapper;
    ITEM *item_ptr;
    ITEM_WRAPPER *owner_ptr;
    int item_offset;

    wrapper.tag = 1234;
    wrapper.item.value = 77;

    item_ptr = &wrapper.item;
    item_offset = (int)__builtin_offsetof(ITEM_WRAPPER, item);
    owner_ptr = CONTAINING_RECORD(item_ptr, ITEM_WRAPPER, item);

    BeaconPrintf(CALLBACK_OUTPUT,
        "offset=%d tag=%d value=%d",
        item_offset, owner_ptr->tag, owner_ptr->item.value);
}

demo_layout_helpers();
```

---

## 10) VM/ABI Expectations

- Target runtime uses little-endian bytecode assumptions.
- Host/target pointer-size compatibility is enforced at load/runtime boundaries.
- Runtime stack/call/global/local capacities are finite; avoid unbounded recursion and oversized local state.

---

## 11) AI-Agent Generation Checklist

Before finalizing a script, ensure:
1. Includes come from provided interpreter headers.
2. No floating-point dependencies are introduced.
3. `void *` is cast before indexing/dereference.
4. FFI signatures use only allowed atom types.
5. Varargs use non-`stdcall` conventions.
6. Native pointer arguments are passed pointer expressions or null.
7. Bare native function calls are unambiguous (or explicitly `LIB$Func`).
8. Declarators are conservative and implementation-friendly.
9. Struct assignment only occurs between compatible struct types.
10. `__argc`/`__argv` are treated as Beacon packed-argument data, not classic C argv arrays.
11. Existing header definitions are reused before creating new structs/enums/FFI signatures.
12. Duplicate-definition errors are resolved by removing redundant script-local definitions that already exist in included headers.
13. Large output paths use `BeaconFormat` buffering + chunking rather than high-frequency `BeaconPrintf` calls.
14. `BeaconPrintf` is not used inside tight loops for bulk data emission.
15. `_WIN32`/`UNICODE` (when needed) are defined before any includes so header aliasing resolves as intended.

---

## 12) Recommended Authoring Pattern

When generating scripts for this interpreter:
- Prefer straightforward C89-style declarations.
- Prefer explicit casts and explicit types.
- Prefer implementation-proven idioms from `interpreter-includes/` APIs.
- Parse all runtime arguments through Beacon data APIs.

This approach maximizes cross-session compatibility with Cobalt Strike Interpreter execution paths.
