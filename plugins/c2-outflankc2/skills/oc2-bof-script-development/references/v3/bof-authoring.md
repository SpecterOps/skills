# OC2 V3 BOF Authoring Model

## Packaging

Typical single-command layout:

```
mytool/
  MyTool.x64.o
  oc2/
    pyproject.toml
    uv.lock
    manifest.json
    mytool.py
```

`pyproject.toml` should match released apps:

```toml
[project]
name = "oc2-commands-mytool"
version = "1.0.0"
description = "Example BOF command provider"
requires-python = "==3.13.11"
dependencies = [
    "oc2-sdk-python==3.0.0-rc.1",
]

[tool.uv.sources]
oc2-sdk-python = { index = "outflank-jfrog-customer" }

[[tool.uv.index]]
name = "outflank-jfrog-customer"
url = "https://outflank.jfrog.io/artifactory/api/pypi/pypi-customer/simple"
explicit = true
```

Generate and include `oc2/uv.lock` before packaging the application:

```bash
cd oc2
uv lock
```

OC2 requires both `pyproject.toml` and `uv.lock` for `uv-python` applications and installs the locked environment with `uv sync --frozen`. Regenerate the lock file whenever the project dependencies change.

Declare the object file as a manifest artifact (`type: "bof"`). `_metadata.min_api_version` is `"3.0.0-rc.1"`.

```json
{
  "package_id": "nl.example.mytool",
  "version": "1.0.0",
  "display_information": {
    "name": "MyTool",
    "description": "Example BOF command"
  },
  "_metadata": {
    "schema_version": "1.0.0",
    "min_api_version": "3.0.0-rc.1"
  },
  "runtime": {
    "type": "uv-python",
    "working_dir": "{root_dir}/oc2",
    "command": ["{python}", "mytool.py"],
    "autostart": true,
    "autorestart": "unexpected",
    "startretries": 5,
    "exitcodes": [0, 2]
  },
  "artifacts": [
    {
      "name": "mytool_bof_x64",
      "path": "{root_dir}/MyTool.x64.o",
      "type": "bof"
    }
  ],
  "features": {
    "command_provider": {}
  }
}
```

Multi-arch: one artifact per object (`mytool_bof_x64`, `mytool_bof_x86`) and matching `CommandSupport` entries. Pick the name at runtime from `ctx.implant.architecture_type`.

### Installation and discovery

Unlike V2, V3 does not discover wrappers by scanning `shared/bofs`. A V3 command becomes available after its command-provider process connects to OC2 and registers the decorated handlers added with `app.command_provider.add_commands_from_module(...)` before `Application.run()`.

- OC2-hosted: Create a ZIP containing the layout above with exactly one `manifest.json`, then upload it under Applications in the OC2 GUI. Supply the Outflank JFrog credentials when prompted. OC2 validates the manifest and bundled artifact paths, runs `uv sync --frozen`, injects command-provider authentication and `OC2_APPLICATION_ROOT_DIR`, and starts `runtime.command` under supervision.
- Self-hosted or local development: Register the application in the OC2 GUI, make the JFrog credentials available to `uv`, and configure `OC2_SERVER_URL` plus either the one-time `OC2_APPLICATION_BOOTSTRAP_TOKEN` or an existing `OC2_ACCESS_TOKEN`. Start the provider from the manifest directory:

  ```bash
  cd mytool/oc2
  uv sync --frozen
  uv run python mytool.py
  ```

The manifest `package_id` and `version` must match the application registered on the server. On the first self-hosted run, the SDK exchanges the bootstrap token for an access token and caches it for later runs.

## Lifecycle

1. Parse operator input (`DefaultArgumentParser` + `ctx.split_and_parse_arguments`). `None` means help or a parse error was already handled.
2. Read the manifest BOF with `read_manifest_artifact` and `upsert_artifact` (provider-shipped object).
3. Pack BOF arguments with `bof_pack` or `bof_pack_for_task`.
4. Schedule the documented V3 task with `ctx.schedule_task(name="exec_bof"|"exec_bof_async", ...)`.

V2's `exec_bof_non_threaded` task name is not documented by the supplied V3 SDK or server. Use it in V3 only after verifying support in the target implant/Stage1; see the compatibility warning in the runtime API reference.

The BOF object is always `TaskBinaryItem` id 0. Extra binaries start at 1. IDs must be unique.

`CommandSupport` hides the command from unsupported OS/arch combinations. It does not enforce privilege. Check privilege/integrity explicitly (for example `ImplantsApi` + `is_admin`) when the BOF requires High / admin.

Operator `@artifacts/name` refs are catalog uploads, not manifest files. Resolve with `ctx.fetch_artifact` (metadata only). Do not download and re-upsert those bytes to pass them to the BOF.

## Practical Guidance

### Status vs output

Typical wrappers are fire-and-forget: schedule the BOF and return. The implant streams BOF output. Do not copy that stream into `ctx.output`.

- `ctx.status.*` — execution lifecycle (`failed` for wrapper validation)
- `ctx.output.*` — wrapper messages only

Wait (`wait_for_task_response`) when the provider must act on the result: parse a listing, persist rows via REST, or build a structured observation. Builtin `ls` does this for native file listings (`wait` then `FilesApi`). A BOF that emits list-like text uses the same wait-then-parse shape (for example an LDAP or directory listing BOF).

```python
import asyncio

from oc2_sdk_python.command import CommandCancelledException
from oc2_sdk_python.task import ImplantTaskState


task = await ctx.schedule_task(name="exec_bof", argument_list=[packed], binaries=[...])
await ctx.status.running("Waiting for BOF output", progress=0.5)

try:
    response = await ctx.wait_for_task_response(
        task_uid=task.uid,
        with_status=False,
    )
except CommandCancelledException:
    await ctx.status.cancelled("Command execution cancelled")
    return
except asyncio.TimeoutError:
    message = "Timeout while waiting for BOF output"
    await ctx.status.timeout(message)
    await ctx.output.error(message)
    return

try:
    state = ImplantTaskState(response.state)
except ValueError:
    message = f"Task {task.uid} returned unknown state: {response.state!r}"
    await ctx.status.failed(message)
    await ctx.output.error(message)
    return

if state == ImplantTaskState.CANCELLED:
    await ctx.status.cancelled(f"Task {task.uid} cancelled")
    return

if state == ImplantTaskState.ERROR:
    message = (response.response or "").strip() or f"Task {task.uid} failed"
    await ctx.status.failed(message)
    await ctx.output.error(message)
    return

if state != ImplantTaskState.FINISHED:
    message = f"Task {task.uid} ended in unexpected state {state.value}"
    await ctx.status.failed(message)
    await ctx.output.error(message)
    return

# Only parse response.response or perform a REST upsert after FINISHED.
await ctx.status.completed("Done")
```

Use `with_status=False` when the provider owns the wait and terminal statuses, as above. Never parse or persist `response.response` before confirming `ImplantTaskState.FINISHED`.

Fire-and-forget remains the default.

### Collections

Multi-command apps use a shared helper (read/upsert/pack/schedule). Do not invent a second packaging model.

### GUI

GUI elements/dialogs are currently unsupported in OC2 V3.
