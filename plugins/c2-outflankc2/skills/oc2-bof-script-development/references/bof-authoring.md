# OC2 BOF Authoring Model

## Packaging

OC2 discovers BOF wrappers by scanning `shared/bofs` for files matching the `_bof.s1.py` suffix (e.g. `sample_bof.s1.py`). A command named `sample` resolves architecture-specific object files such as `sample.x86.o`, `sample.x64.o`, or `sample.arm64.o` from the task base path.

Use `base_binary_name` when the command and object stem differ, and `base_binary_path` for a subdirectory. Override `_get_base_binary_name()` only for validated, argument-driven variants.

## Lifecycle Hooks

| Hook | Purpose |
|---|---|
| `split_arguments()` | Preserve a single path or customize tokenization. |
| `rewrite_arguments()` | Normalize operator input before validation. |
| `validate_arguments()` | Add semantic or cross-field validation. |
| `validate_binary_content()` | Validate the BOF binary (size limits, COFF header check). |
| `validate_files()` | Validate uploaded task files. |
| `_encode_arguments_bof()` | Return typed BOF arguments in ABI order. |
| `run()` | Add response text or tasks before/after execution. |
| `rewrite_response()` | Normalize returned output. |
| `get_gui_elements()` | Describe an optional OC2 GUI form. |

The normal flow is split, rewrite, validate, validate binary/files, run, execute, and rewrite response. Parent `run()` enforces target restrictions, encodes arguments, selects the OC2 execution command, and loads the object file.

## Practical Guidance

- Use `argparse` choices and types for local validation.
- Parse named arguments inside the encoder instead of depending on raw indexes when options are present.
- Keep response transformations deterministic and handle `None`.
- Restrict dynamic binary names to an allowlist so input cannot become a path.
