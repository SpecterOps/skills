# OC2 V2 BOF Runtime API

## Constructor

```python
BaseBOFTask(
    name,
    base_binary_name=None,
    base_binary_path=None,
    parser_prefix_chars=None,
    min_privilege=None,
    supported_architectures=None,
    supported_os=[ImplantOSType.WINDOWS],
    bof_type=BOFType.DEFAULT,
)
```

Relevant enum values:

- `ImplantArch`: `INTEL_X86`, `INTEL_X64`, `ARM64`
- `ImplantOSType`: `WINDOWS`, `MAC_OS`, `LINUX`
- `ImplantPrivilege`: `UNTRUSTED`, `LOW`, `MEDIUM`, `HIGH`, `SYSTEM`, `PROTECTED_PROCESS`
- `BOFType`: `DEFAULT`, `DEFAULT_NON_THREADED`, `ASYNC`

The deprecated `non_threaded` constructor flag maps `DEFAULT` to `DEFAULT_NON_THREADED`; prefer `bof_type`.

## Argument Packing

`_encode_arguments_bof()` returns `(BOFArgumentEncoding, value)` tuples.

| Encoding | Value | Wire value |
|---|---|---|
| `WSTR` | `str` | Length-prefixed NUL-terminated UTF-16LE |
| `STR` | `str` | Length-prefixed NUL-terminated UTF-8 |
| `BUFFER` | `bytes` | Length-prefixed bytes |
| `INT` | integer | Signed 32-bit little-endian |
| `SHORT` | integer | Signed 16-bit little-endian |

OC2 preserves tuple order, prepends the total packed length, and base64-encodes the buffer.

## Binary and Execution Selection

| Architecture | Default suffix |
|---|---|
| x86 | `.x86.o` |
| x64 | `.x64.o` |
| ARM64 | `.arm64.o` |

| BOF type | Outgoing task |
|---|---|
| `DEFAULT` | `exec_bof` |
| `DEFAULT_NON_THREADED` | `exec_bof_non_threaded` |
| `ASYNC` | `exec_bof_async` |

Common imports:

```python
from outflank_stage1.implant.enums import ImplantArch, ImplantOSType, ImplantPrivilege
from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding, BOFType
from outflank_stage1.task.exceptions import TaskInvalidArgumentsException
```
