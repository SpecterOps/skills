# OC2 V3 BOF Wrapper Examples

Pinned to `oc2-sdk-python==3.0.0-rc.1` (beta). Later release candidates may introduce breaking changes. Every architecture-specific example sets `CommandSupport`.

## Minimal Wrapper

Manifest artifact name `env_bof_x64` maps to `{root_dir}/env.x64.o`.

```python
import asyncio
import logging
import sys

from oc2_sdk_python.application import Application, read_manifest_artifact
from oc2_sdk_python.artifacts import upsert_artifact
from oc2_sdk_python.command import (
    CommandContext,
    CommandSupport,
    DefaultArgumentParser,
    command,
)
from oc2_sdk_python.logging import configure_logging
from oc2_sdk_python.task import TaskBinaryItem
from oc2_sdk_python.types import Architecture, OperatingSystem

BOF_NAME = "env_bof_x64"


@command(
    name="env",
    description="List environment variables.",
    support=[CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)],
)
async def env(ctx: CommandContext) -> None:
    parser = DefaultArgumentParser(prog="env", description="List environment variables.")
    if await ctx.split_and_parse_arguments(parser=parser) is None:
        return

    bof_bytes = await asyncio.to_thread(read_manifest_artifact, BOF_NAME)
    artifact_id, _ = await upsert_artifact(ctx.api_client, name=BOF_NAME, data=bof_bytes)

    await ctx.schedule_task(
        name="exec_bof",
        binaries=[TaskBinaryItem(id=0, label="bof", artifact_id=artifact_id)],
    )


async def register() -> None:
    configure_logging(logging.DEBUG)
    app = Application()
    app.command_provider.add_commands_from_module(sys.modules[__name__])
    await app.run()


def main() -> None:
    asyncio.run(register())


if __name__ == "__main__":
    main()
```

## Constrained Typed Argument

```python
import asyncio
import logging
import sys

from oc2_sdk_python.api_client.api.implants_api import ImplantsApi
from oc2_sdk_python.application import Application, read_manifest_artifact
from oc2_sdk_python.artifacts import upsert_artifact
from oc2_sdk_python.bof import bof_pack
from oc2_sdk_python.command import (
    CommandContext,
    CommandSupport,
    DefaultArgumentParser,
    command,
)
from oc2_sdk_python.logging import configure_logging
from oc2_sdk_python.task import TaskBinaryItem
from oc2_sdk_python.types import Architecture, OperatingSystem

BOF_NAME = "untrustprocess_bof_x64"


@command(
    name="untrustprocess",
    description="Lower a process token integrity level.",
    support=[CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)],
)
async def untrustprocess(ctx: CommandContext) -> None:
    parser = DefaultArgumentParser(
        prog="untrustprocess",
        description="Lower a process token integrity level.",
        epilog="Example: untrustprocess 1337\nExample: untrustprocess firefox.exe",
    )
    parser.add_argument("process", help="PID or process name.")
    args = await ctx.split_and_parse_arguments(parser=parser)
    if args is None:
        return

    implant_response = await ImplantsApi(ctx.api_client).implants_get_implant_by_uid(
        implant_uid=ctx.implant.implant_uid,
    )
    if implant_response.implant.is_admin is not True:
        message = "Requires admin privileges."
        await ctx.status.failed(message)
        await ctx.output.error(message)
        return

    bof_bytes = await asyncio.to_thread(read_manifest_artifact, BOF_NAME)
    artifact_id, _ = await upsert_artifact(ctx.api_client, name=BOF_NAME, data=bof_bytes)
    packed = bof_pack([("WSTR", args.process)])

    await ctx.schedule_task(
        name="exec_bof",
        argument_list=[packed],
        binaries=[TaskBinaryItem(id=0, label="bof", artifact_id=artifact_id)],
    )


async def register() -> None:
    configure_logging(logging.DEBUG)
    app = Application()
    app.command_provider.add_commands_from_module(sys.modules[__name__])
    await app.run()


def main() -> None:
    asyncio.run(register())


if __name__ == "__main__":
    main()
```

Privilege is not expressed via `CommandSupport`. This example preserves the V2 High / admin requirement with an explicit `ImplantsApi` check and fails before scheduling when `implant.is_admin` is false or unknown.

## Catalog BUFFER

Operator passes `@artifacts/input.bin`. Do not download or re-upsert those bytes. Manifest BOF name `process_file_bof_x64` must match `CommandSupport` x64.

```python
import asyncio

from oc2_sdk_python.application import read_manifest_artifact
from oc2_sdk_python.artifacts import upsert_artifact
from oc2_sdk_python.bof import BofArgumentEncoding, bof_pack
from oc2_sdk_python.command import (
    CommandContext,
    CommandSupport,
    DefaultArgumentParser,
    command,
)
from oc2_sdk_python.task import TaskBinaryItem
from oc2_sdk_python.types import Architecture, OperatingSystem

BOF_ARTIFACT_NAME = "process_file_bof_x64"
INPUT_BINARY_ID = 1


@command(
    name="process_file",
    description="Pass an existing catalog artifact to a BOF",
    support=[CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)],
)
async def process_file(ctx: CommandContext) -> None:
    parser = DefaultArgumentParser(prog="process_file")
    parser.add_argument(
        "artifact",
        help="Artifact reference, for example @artifacts/input.bin",
    )

    args = await ctx.split_and_parse_arguments(parser=parser)
    if args is None:
        return

    if not args.artifact.startswith("@artifacts/"):
        await ctx.status.failed(
            "Expected an artifact reference such as @artifacts/input.bin"
        )
        return

    # Metadata only; does not download the catalog bytes.
    artifact = await ctx.fetch_artifact(args.artifact)
    if artifact is None:
        await ctx.status.failed(f"Artifact not found: {args.artifact}")
        return

    bof_bytes = await asyncio.to_thread(read_manifest_artifact, BOF_ARTIFACT_NAME)
    bof_artifact_id, bof_artifact_name = await upsert_artifact(
        ctx.api_client,
        name=BOF_ARTIFACT_NAME,
        data=bof_bytes,
    )

    packed_arguments = bof_pack(
        [
            (
                BofArgumentEncoding.BUFFER,
                INPUT_BINARY_ID.to_bytes(4, byteorder="little", signed=False),
            ),
        ]
    )

    task = await ctx.schedule_task(
        name="exec_bof",
        argument_list=[packed_arguments],
        binaries=[
            TaskBinaryItem.from_artifact(
                bof_artifact_id,
                id=0,
                label=bof_artifact_name,
            ),
            TaskBinaryItem.from_artifact(
                artifact.id,
                id=INPUT_BINARY_ID,
                label=artifact.name,
            ),
        ],
    )

    await ctx.status.completed(f"Scheduled task {task.uid}")
```

A 4-byte BUFFER is a candidate binary id. The implant substitutes the attached binary only if that id exists; otherwise the 4 bytes stay inline. Do not attach another binary whose id equals a genuine 4-byte inline BUFFER value.

If you already have the bytes, `bof_pack_for_task` offloads large `BUFFER`s to ids `1+`. If you only have a catalog artifact id, use this example (`from_artifact` and a 4-byte BUFFER).

## Variations

| Pattern | Approach |
|---|---|
| Subcommands as opcodes | Map CLI verbs to `SHORT`/`INT`, then `bof_pack` (chromeo / coercer). |
| Pass-through command line | Validate first: `raw_arguments = ctx.arguments or ""`. If empty when required, show help. Then `bof_pack([("WSTR", raw_arguments)])`. Never pack `ctx.arguments` raw. |
| Multi-arch | `CommandSupport` for each arch; pick `{stem}_bof_x64` / `_x86` from `ctx.implant.architecture_type`. Do not pack unused CLI-only flags. |
| Inline / priv-esc | V2 used `exec_bof_non_threaded`, but the supplied V3 SDK and server do not document that task name. Use it only after verifying support in the target V3 implant/Stage1; do not silently substitute `exec_bof`. |
| Wait / parse | Fire-and-forget is default. Wait when the provider must parse or persist (listings, LDAP). See the wait snippet in the authoring ref. |
| Provider needs catalog bytes | Download in the provider only if Python needs the bytes. If the BOF needs them, use the 4-byte BUFFER + `from_artifact` pattern. |
