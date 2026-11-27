# Validation

## Authoring checks

Review these representative requests after changing the skill. They exercise
decisions that packaging checks cannot prove. Record the generated answer and
whether it meets the criteria; a manifest check is not a behavioral evaluation.

| Request | Expected behavior |
| --- | --- |
| Write a script that prints one packed string argument. | Use the Beacon data APIs and check the supplied buffer; do not treat `__argc` as an argument count. Include top-level entry logic. |
| Review a script with an uncalled `main()`, POSIX `argv` indexing, and floating-point math. | Identify all three incompatibilities and propose focused corrections. |
| Use `GetCurrentProcessId` in a script. | Find the existing declaration through the bundled headers and reuse it. Keep includes as header names. |
| Adapt a native CRT varargs call for a 32-bit target. | Define `_WIN32` before includes and preserve the native `cdecl` declaration. Do not introduce script-defined varargs. |
| Review a loop that emits thousands of output events. | Recommend bounded formatting, chunked output, and cleanup. |

Also check that an unrelated ordinary C or Aggressor-only request does not
unnecessarily select this skill.

## Interpreter checks

The support snapshot currently records no runtime validation. When the user
requests runtime testing, record the Cobalt Strike build, target architecture,
Team Server header version, exact script and argument format, compilation
result, and observed output. Exercise each architecture before claiming support
for it. A C compiler or a language server cannot validate the interpreter's
custom FFI declarations and top-level statements.

Start with the bundled demo and a small packed-argument example in a suitable
test environment. For x86, apply the documented architecture selection before
includes. Do not assume the demo's native function calls are pure compilation
tests. Runtime checks are separate from offline package validation.

Keep portable validation summaries in the repository's compatibility record.
Do not include target identifiers or operational logs in distributed resources.
