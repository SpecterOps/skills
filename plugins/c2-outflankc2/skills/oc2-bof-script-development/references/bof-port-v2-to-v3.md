# Porting OC2 version 2 BOF scripts to version 3

Pinned to `oc2-sdk-python==3.0.0-rc.1` and OC2 API `3.0.0-rc.1` (beta). Later release candidates may introduce breaking changes. Also read the V3 authoring and runtime refs.

Policy: `*_bof.s1.py` cannot be reused. Rewrite as a command-provider application. Ignore leftover `.s1.py` files in dual-shipped repos.

## Pre-port audit

Rewrite the V2 class as a V3 command-provider application (`@command`, manifest artifacts, `schedule_task`). Do not mechanically translate constructor + parser + `_encode_arguments_bof`.

Inspect the complete V2 class first. Carry over anything you find:

- Constructor `base_binary_name` / `base_binary_path`
- Constructor `parser_prefix_chars`
- `min_privilege`
- Effective `supported_architectures` / `supported_os`, including inherited defaults. A V2 class that omits `supported_os` is still Windows-only because `BaseBOFTask` defaults to `[ImplantOSType.WINDOWS]`.
- `BOFType` including `DEFAULT_NON_THREADED` and `ASYNC` (also deprecated `non_threaded=True`)
- Parser description, epilog, prefix characters, choices, types, defaults, and argument order
- Custom `split_arguments`
- `rewrite_arguments`
- `_get_base_binary_name`, `_get_base_binary_path`, or suffix selection
- `validate_*` methods
- Custom `run()`
- `append_response` / `rewrite_response`
- Tasks scheduled before or after the BOF (`add_task_before` / `add_task_after`)
- License-expiry behavior
- `get_gui_elements()`

## Hook map

| V2 | V3 |
|---|---|
| `class X(BaseBOFTask)` | `@command` + `async def` |
| Constructor `base_binary_name` / `base_binary_path` | Manifest `artifacts[]` names and paths. Preserve the effective object-file location even when the V2 class did not override `_get_base_binary_name()` or `_get_base_binary_path()`. |
| `supported_architectures` / `supported_os` | Explicit `CommandSupport` OS/architecture pairs. Compute the effective V2 restrictions, including inherited defaults: omitted V2 `supported_os` means Windows-only, while omitted V3 `support` offers the command on every OS/architecture combination. Enumerate each supported architecture that has a matching BOF artifact. Map V2 `ImplantOSType.MAC_OS` to V3 `OperatingSystem.MACOS`. |
| `min_privilege` | Explicit runtime check using `ImplantsApi`; `CommandSupport` does not enforce privilege. For Windows, compare `implant.integrity_level_windows` with the matching MIC RID. `implant.is_admin` is a shortcut only for a `HIGH`-or-above requirement. |
| Constructor `parser_prefix_chars` | Pass the compatible prefix set as `DefaultArgumentParser(prefix_chars=...)`. The V3 default parser installs `-h` / `--help`, so `-` must remain a prefix; if the V2 surface excluded `-`, use a custom `AbstractArgumentParser` or explicitly document and test the changed help surface. |
| Parser description / epilog / `self.parser.add_argument` | `DefaultArgumentParser(description=..., epilog=...)` + `add_argument` + `split_and_parse_arguments`. Preserve choices, types, defaults, option names, positional order, and required/optional behavior. |
| Custom `split_arguments` | Implement `AbstractArgumentSplitter` and pass it to `ctx.split_arguments` or `ctx.split_and_parse_arguments`. For deliberately unsplit input, use `ctx.arguments` directly or return the entire string as one token. |
| `rewrite_arguments` | Split first, normalize the token list explicitly, then call `ctx.parse_arguments`. Do not use the combined `split_and_parse_arguments` helper when normalization must occur between those steps. |
| `validate_arguments` | Let the V3 parser handle syntax, then perform custom semantic and cross-field checks in the handler. On failure, set `ctx.status.failed`, emit a useful error, and return before scheduling. |
| `validate_binary_content` | Validate the resolved BOF bytes explicitly after `read_manifest_artifact` or artifact download and before `upsert_artifact` / `schedule_task`. V3 does not invoke this hook automatically. |
| `validate_files` | Replace V2 task files with manifest, catalog, or generated `TaskBinaryItem` sources. Validate artifact metadata after `ctx.fetch_artifact`; download through `ArtifactsApi.artifacts_download_artifact_by_id` first when content must be inspected. Return before scheduling on failure. |
| `_encode_arguments_bof` tuples | `bof_pack` / `bof_pack_for_task` |
| `{stem}.{arch}.o` plus name/path/suffix hooks | Manifest `artifacts[]` + runtime artifact-name selection |
| `BOFType.DEFAULT` | `schedule_task(name="exec_bof")` |
| `BOFType.DEFAULT_NON_THREADED` or `non_threaded=True` | No SDK-documented V3 equivalent. V2 used `exec_bof_non_threaded`, but the supplied V3 SDK and server do not document that task name. Verify support in the target V3 implant/Stage1 before retaining it. Do not silently map to `exec_bof`, because that changes the execution mode. |
| `BOFType.ASYNC` | `schedule_task(name="exec_bof_async")` |
| Parent `run()` schedules the BOF | Explicit `ctx.schedule_task(...)` |
| Custom `run()` | Move its behavior into the async command handler, preserving its position after validation and before or around `ctx.schedule_task`. Replace V2 exceptions/error responses with explicit output, terminal status, and an early return. |
| `append_response` | Emit static wrapper-generated text with `ctx.output.*`. Waiting is only necessary when the appended text depends on the implant response. |
| `rewrite_response` | Wait with `wait_for_task_response`, handle cancellation and timeout, require `ImplantTaskState.FINISHED`, then transform and emit the response. |
| Extra tasks around the BOF | Schedule those implant tasks explicitly in the handler |
| License-expiry behavior | There is no automatic V3 equivalent. Recreate a per-command check before scheduling, or raise `ApplicationFatalError` during startup only when expiry makes the entire provider unusable. Preserve the exact V2 behavior: a missing or non-file `license_time` means not expired, malformed contents mean expired, and an elapsed timestamp means expired. |
| `get_gui_elements()` | Unsupported in V3 for this skill. Tell the user performing the port, then omit the dialog. Do not recreate V2 dialogs another way. Do not silently drop. |

Do not infer that a missing V2 `supported_os` declaration means unrestricted support. For example, a V2 class that only sets `supported_architectures=[ImplantArch.INTEL_X64]` is effectively Windows x64 and must become `CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)`. Because `CommandSupport` has no OS-only wildcard, a Windows BOF supporting multiple architectures needs one entry per architecture and a corresponding manifest artifact for each entry.

V2 invoked the hooks in this order: `split_arguments` -> `rewrite_arguments` -> `validate_arguments` -> `validate_binary_content` -> `validate_files` -> `run`. V3 invokes none of them automatically. Preserve the same dependencies explicitly in the command handler. When rewriting must happen before parser validation, use the separate context methods:

```python
tokens = ctx.split_arguments(ctx.arguments, splitter=CustomSplitter())
tokens = rewrite_arguments(tokens)

args = await ctx.parse_arguments(tokens, parser=parser)
if args is None:
    return

try:
    validate_arguments(args, ctx)
    bof_bytes = await asyncio.to_thread(read_manifest_artifact, bof_name)
    validate_binary_content(bof_bytes, ctx.implant)
except ValueError as exc:
    message = str(exc)
    await ctx.status.failed(message)
    await ctx.output.error(message)
    return

# Resolve and validate any additional payloads here, then pack and schedule.
```

The helper names in this skeleton are port-specific functions, not SDK hooks. Keep blocking filesystem or CPU-heavy validation off the event loop with `asyncio.to_thread`. For an operator-managed `@artifacts/...` input, `ctx.fetch_artifact` returns metadata (`id`, names, and size), not its content. Metadata-only validation can use that result directly; content validation requires `ArtifactsApi(ctx.api_client).artifacts_download_artifact_by_id(artifact_id=artifact.id)` before constructing `TaskBinaryItem.from_artifact(...)`.

For migrated license checks, distinguish the V2 wrapper's own bundled/vendor license policy from OC2 server licensing. Preserve the V2 wrapper's exact handling of `license_time`: treat a missing path or a path that is not a file as not expired, treat contents that cannot be parsed as an integer timestamp as expired, and treat a timestamp earlier than the current time as expired. A command-scoped expiry should emit an error, set `ctx.status.failed`, and return. Reserve `ApplicationFatalError` for an unrecoverable application-wide condition because it stops the command-provider application.

When response-dependent behavior requires a wait, catch both `CommandCancelledException` and `asyncio.TimeoutError`. Check the returned `ImplantTaskState` before parsing: map `CANCELLED` to `ctx.status.cancelled`, map `ERROR` and unknown or unexpected states to `ctx.status.failed`, and post-process only `FINISHED`. Use the complete wait pattern in the [V3 authoring reference](v3/bof-authoring.md#status-vs-output) rather than assuming that a returned response is successful.

For Windows implants, map V2 minimum privileges to V3 mandatory integrity control (MIC) RIDs:

| V2 `ImplantPrivilege` | Minimum `integrity_level_windows` |
|---|---:|
| `UNTRUSTED` | `0x0000` |
| `LOW` | `0x1000` |
| `MEDIUM` | `0x2000` |
| `HIGH` | `0x3000` |
| `SYSTEM` | `0x4000` |
| `PROTECTED_PROCESS` | `0x5000` |

Treat a null `integrity_level_windows` as unknown: do not schedule a command whose minimum privilege cannot be confirmed. The field is null when the Windows integrity level is unknown and on non-Windows implants. For `HIGH`, `implant.is_admin is True` is equivalent to `integrity_level_windows >= 0x3000`; use the numeric field when the port must preserve another V2 threshold.

## Argument-packing wire change

Keep the logical tuple order and types from V2, but repack them with the V3 SDK. The base64-decoded formats are incompatible:

| Version | Decoded layout |
|---|---|
| V2 | 4-byte little-endian total length, then values in ABI order. Strings and buffers carry their own lengths; integers and shorts are fixed width. There is no per-argument type field. |
| V3 | 2-byte message type `7`, 2-byte version `1`, 4-byte total message length, then one TLV per argument: 4-byte encoding, 4-byte value length, and value bytes. |

`bof_pack` constructs the complete V3 message and returns its base64 representation. `bof_pack_for_task` uses the same message format, but can replace large `BUFFER` values with 4-byte `TaskBinaryItem` ids. Never reuse V2's `_bof_arguments_to_base64`, a V2 base64 blob, or a hand-built V2 payload in `argument_list`.

## Side-by-side: untrustprocess

V2 (`untrustprocess_bof.s1.py`):

```python
from typing import List, Tuple

from outflank_stage1.implant.enums import ImplantArch, ImplantPrivilege
from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding


class UntrustProcessBOF(BaseBOFTask):
    def __init__(self):
        super().__init__(
            "untrustprocess",
            min_privilege=ImplantPrivilege.HIGH,
            supported_architectures=[ImplantArch.INTEL_X64],
        )
        self.parser.add_argument("process", help="PID or process name.")
        self.parser.description = "Lower a process token integrity level."

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        return [(BOFArgumentEncoding.WSTR, arguments[0])]
```

V3 (handler + artifact). `CommandSupport` replaces arch/OS. The explicit `ImplantsApi` check preserves the V2 `min_privilege=HIGH` requirement using the Windows high-integrity-or-above `is_admin` shortcut. Manifest artifact:

```json
{
  "name": "untrustprocess_bof_x64",
  "path": "{root_dir}/UntrustProcess.x64.o",
  "type": "bof"
}
```

```python
import asyncio

from oc2_sdk_python.api_client.api.implants_api import ImplantsApi
from oc2_sdk_python.application import read_manifest_artifact
from oc2_sdk_python.artifacts import upsert_artifact
from oc2_sdk_python.bof import bof_pack
from oc2_sdk_python.command import (
    CommandContext,
    CommandSupport,
    DefaultArgumentParser,
    command,
)
from oc2_sdk_python.task import TaskBinaryItem
from oc2_sdk_python.types import Architecture, OperatingSystem

BOF_NAME = "untrustprocess_bof_x64"


@command(
    name="untrustprocess",
    description="Lower a process token integrity level.",
    support=[CommandSupport(OperatingSystem.WINDOWS, Architecture.INTEL_X64)],
)
async def untrustprocess(ctx: CommandContext) -> None:
    parser = DefaultArgumentParser(prog="untrustprocess")
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
```

If the V2 class used `non_threaded=True` or `BOFType.DEFAULT_NON_THREADED`, do not perform a mechanical task-name replacement. The supplied V3 SDK and server do not document `exec_bof_non_threaded`. First verify that the target V3 implant/Stage1 supports it. If support cannot be established, stop and resolve the execution-mode requirement instead of silently substituting `exec_bof`.

## Pass-through command line

When V2 packed the raw operator line as one `WSTR`, keep that surface — but validate:

```python
raw_arguments = ctx.arguments or ""
if not raw_arguments.strip():
    await ctx.output.plain(parser.format_help())
    await ctx.status.completed("Help displayed")
    return
packed = bof_pack([("WSTR", raw_arguments)])
```

Never `bof_pack([("WSTR", ctx.arguments)])` — `ctx.arguments` may be `None`.

## Checklist

- [ ] Manifest artifact names match `read_manifest_artifact` / `upsert_artifact` / `CommandSupport`
- [ ] BOF object is binary id `0`
- [ ] Pack as tuples `("WSTR", val)`, not Cobalt `Z/z/i/s/b`
- [ ] Repack with V3 `bof_pack` / `bof_pack_for_task`; do not reuse a V2 base64 payload or serializer
- [ ] `DEFAULT_NON_THREADED` was not mapped mechanically; target V3 implant/Stage1 support for `exec_bof_non_threaded` was verified before retaining it
- [ ] `ASYNC` becomes `exec_bof_async`
- [ ] Effective V2 OS/architecture restrictions became explicit `CommandSupport` pairs; an omitted V2 `supported_os` was preserved as Windows-only, and every pair has a matching manifest BOF artifact
- [ ] `min_privilege` became a runtime check, using `is_admin` only for `HIGH` or `integrity_level_windows` for the exact V2 threshold; unknown integrity fails closed
- [ ] Constructor `base_binary_name` / `base_binary_path` became the matching manifest artifact name/path, including values inherited without hook overrides
- [ ] Constructor `parser_prefix_chars` and parser description/epilog/options/defaults/order were preserved; any V3 help-prefix change was made explicit and tested
- [ ] Custom `split_arguments` became an `AbstractArgumentSplitter` or intentional raw `ctx.arguments` handling
- [ ] `rewrite_arguments` still runs after splitting and before parser validation
- [ ] Custom `validate_arguments` checks run after parsing and fail before scheduling
- [ ] `validate_binary_content` and `validate_files` became explicit checks over the resolved V3 bytes/artifacts; no inherited validation was assumed
- [ ] Custom `run()` behavior moved into the async handler in the same lifecycle position
- [ ] License-expiry behavior was explicitly preserved as command-scoped failure or application-wide fatal startup validation
- [ ] `get_gui_elements()` flagged to the user and omitted
- [ ] Static `append_response` text became explicit `ctx.output.*`; response-dependent text waits first
- [ ] `rewrite_response` waits, handles cancellation/timeout, checks for `FINISHED`, then transforms output
- [ ] Extra V2 tasks around the BOF scheduled explicitly
- [ ] Do not ship only `*_bof.s1.py`

## Common issues

- Builtin operator `exec_bof` Cobalt Strike encodings are not the wrapper API.
- Existing V3 ports that dropped `non_threaded` are not the pattern to copy when V2 requested inline execution.
- GUI forms have no V3 replacement in this skill.
