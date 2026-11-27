---
name: cobalt-strike-beacon-interpreter
description: Author, review, and troubleshoot Cobalt Strike Beacon Interpreter C scripts, including packed arguments, interpreter headers, and native FFI. Use for Beacon Interpreter script requests and compatibility errors; ordinary compiled BOFs and general Aggressor Script development have separate workflows.
license: Apache-2.0
---

# Beacon Interpreter

Produce C scripts for the Beacon Interpreter dialect using the bundled header
surface. For a review, identify concrete incompatibilities and explain the
smallest corrections. Preserve the user's requested behavior and edit scope.

## Workflow

1. Identify the requested behavior, supplied script, argument format, target
   architecture, and available interpreter version. Read the
   [provenance record](references/provenance.json) before making a version or
   runtime-support claim. If missing target details change the code, ask for
   them; otherwise state the relevant assumptions.
2. Apply the essential rules below. Consult the
   [compatibility guide](references/compatibility.md) for argument packing,
   language restrictions, header selection, FFI, or VM details relevant to the
   request.
3. Search the [bundled headers](references/interpreter-includes/) for the exact
   APIs, structs, and typedefs needed. Read matching declarations and their
   includes before adding definitions. Do not load the entire header collection.
4. Use [interpreter_demo.c](assets/interpreter_demo.c) for examples of supported
   language features and native function pointers. Keep changes specific to the
   requested script. For an Aggressor wrapper, consult the Aggressor development
   skill if it is available and needed; this skill remains usable on its own.
5. Check argument parsing, entry logic, declarations, resource cleanup, output
   volume, and architecture assumptions. Report which checks were actually run.
   Use the [validation guide](references/validation.md) for a runtime check or
   evaluation. Authoring a script does not itself request execution on a Beacon.

All linked paths are relative to this skill directory, independent of the
current working directory or the containing plugin's name.

## Essential compatibility rules

- Entry logic is at top level. A defined `main()` runs only if explicitly called.
- `__argc` is a packed argument buffer's byte length; `__argv` points to that
  buffer. Parse with `BeaconDataParse` and the appropriate Beacon extraction
  functions, not POSIX `argc`/`argv` logic. Match the caller's packing order.
- Use header-name includes such as `#include <windows.h>` and
  `#include <beacon.h>`. The Team Server resolves them against its installed
  interpreter headers. Bundled paths are lookup aids, not script include paths.
- Reuse provided types and native declarations. Remove redundant definitions
  when an included header already supplies them.
- Define `_WIN32` for a 32-bit target and `UNICODE` when Unicode aliases are
  needed, before includes. The guide describes default 64-bit/ANSI selection;
  this is not evidence that a particular target has been tested.
- Avoid `float`/`double`; cast `void *` before dereferencing or indexing it.
  Prefer pointer-based aggregate parameters and simple declarators/macros.
- Native declarations use `LIB$Function: [convention] return_type (types);`.
  Use only the documented FFI atoms. Native varargs require `cdecl`; correct
  calling conventions matter on x86. Script functions do not support varargs
  or calls through function pointers. The demo's function pointer calls a
  native function.
- For large output, use bounded `BeaconFormat` buffers and controlled chunks,
  with cleanup. Avoid high-volume `BeaconPrintf` calls inside tight loops.

## Deliverable

Provide the requested script or review, its expected packed arguments and
architecture assumptions, and concise validation results. Distinguish static
inspection from interpreter compilation and runtime execution. Diagnose errors
against the target's version and header set when they differ from this snapshot.

The bundled resources retain their [Apache-2.0 license](LICENSE).
