# OC2 V3 BOF Runtime API

## Command registration

```python
@command(
    name="mytool",
    description="...",
    support=[CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)],
)
async def mytool(ctx: CommandContext) -> None:
    ...
```

`CommandSupport` is required whenever the BOF is OS/arch specific. Without it the command is offered on every implant.

```python
parser = DefaultArgumentParser(prog="mytool", description="...")
parser.add_argument(...)
args = await ctx.split_and_parse_arguments(parser=parser)
if args is None:
    return
```

## Argument packing

```python
from oc2_sdk_python.bof import BofArgumentEncoding, bof_pack, bof_pack_for_task
```

`bof_pack([(encoding, value), ...])` returns one base64 blob for `argument_list`. Tuple order is the BOF ABI order.

After base64 decoding, the V3 blob is one message header followed by an ordered sequence of argument TLVs:

```text
message type (2-byte LE, 7)
message version (2-byte LE, 1)
total message length (4-byte LE, including the 8-byte header)
repeat for each argument:
    encoding (4-byte LE)
    value length (4-byte LE)
    value bytes
```

The TLV value bytes are:

| Encoding | Code | Python value | Value bytes |
|---|---:|---|---|
| `WSTR` | `10` | `str` | NUL-terminated UTF-16LE |
| `STR` | `20` | `str` | NUL-terminated UTF-8 |
| `BUFFER` | `30` | `bytes` | Bytes unchanged (see 4-byte rule) |
| `INT` | `40` | `int` | Signed 32-bit little-endian |
| `SHORT` | `50` | `int` | Signed 16-bit little-endian |

Use **tuples** `("WSTR", val)` or `BofArgumentEncoding.WSTR`. Not Cobalt `Z/z/i/s/b` type strings (those are the builtin operator `exec_bof` CLI only).

Always construct packed arguments with the SDK rather than hand-building the serialized message.

### Four-byte BUFFER contract

A 4-byte BUFFER is a **candidate** binary reference:

- The implant interprets it as a little-endian unsigned ID.
- It substitutes the attached binary **only when a matching `TaskBinaryItem` id exists**.
- If no matching binary exists, the 4 bytes remain **inline data**.

**Collision:** a genuine 4-byte inline BUFFER whose integer value matches another attached binary ID can be substituted unintentionally. ID **0** is reserved for the BOF object. Extra binaries start at **1**. IDs must be unique.

### `bof_pack` vs `bof_pack_for_task`

- If you have the bytes and a large `BUFFER` should be offloaded, use `bof_pack_for_task`. The SDK writes the 4-byte id and returns extra `TaskBinaryItem`s (ids `1+`).
- If you only have a catalog artifact id, do not use `bof_pack_for_task`. Attach `TaskBinaryItem.from_artifact(artifact.id, id=N)` and pack `BUFFER` = `N.to_bytes(4, "little", signed=False)`.

`bof_pack_for_task` defaults:

- `BUFFER` values of 64 bytes or fewer remain inline in the TLV.
- Larger `BUFFER` values become `TaskBinaryItem`s, starting at id `1`; the TLV contains the 4-byte id.
- Offloaded values of 65,536 bytes or fewer use inline task-binary content. Larger values use an upload session.

The keyword arguments `buffer_inline_threshold`, `first_buffer_payload_id`, and `max_inline_payload_bytes` override those defaults. If the task also attaches binaries manually, set `first_buffer_payload_id` high enough to avoid duplicate ids.

## Binary and Execution Selection

### Binaries

```python
bof_bytes = await asyncio.to_thread(read_manifest_artifact, "mytool_bof_x64")
artifact_id, _ = await upsert_artifact(ctx.api_client, name="mytool_bof_x64", data=bof_bytes)

await ctx.schedule_task(
    name="exec_bof",
    argument_list=[packed],  # omit if the BOF takes no args
    binaries=[
        TaskBinaryItem(id=0, label="bof", artifact_id=artifact_id),
    ],
)
```

Catalog refs: `ctx.fetch_artifact("@artifacts/...")` returns **metadata only**. Then `TaskBinaryItem.from_artifact(artifact.id, id=N, label=artifact.name)`.

### Implant opcodes

Choose the execution mode with `schedule_task(name=...)`:

| Name | When |
|---|---|
| `exec_bof` | Default. New thread, full exception handling (stability). |
| `exec_bof_async` | Long-running. Stop with `cancel` + task UID; tag the task to find it. |

The current V3 SDK and server documentation define only `exec_bof` and `exec_bof_async`. V2 also used `exec_bof_non_threaded`, but that task name is not documented by the supplied V3 SDK or server. Treat it as implant-dependent: use it only after verifying that the target V3 implant/Stage1 supports the opcode. Do not assume support from V2 or silently replace it with `exec_bof`, because changing the execution mode can change behavior.

## Common imports

```python
from oc2_sdk_python.application import Application, read_manifest_artifact
from oc2_sdk_python.artifacts import upsert_artifact
from oc2_sdk_python.bof import BofArgumentEncoding, bof_pack, bof_pack_for_task
from oc2_sdk_python.command import (
    CommandContext,
    CommandSupport,
    DefaultArgumentParser,
    command,
)
from oc2_sdk_python.task import TaskBinaryItem
from oc2_sdk_python.types import Architecture, OperatingSystem
```
