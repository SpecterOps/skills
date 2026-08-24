# OC2 Bot Runtime API

## Events

| Handler | Value |
|---|---|
| `on_new_implant(implant)` | New `Implant` |
| `on_implant_checkin(implant)` | Existing `Implant` check-in |
| `on_task_request(task)` | Requested `BaseTask` |
| `on_task_response(task)` | Responding `BaseTask` |

Task events carry an implant UID, not an `Implant`. Resolve current details with `ImplantService`.

## Services

### TaskService

```python
from outflank_stage1.services.task_service import TaskService

TaskService().schedule_task(implant_uid=uid, task=task)
```

### ImplantService

```python
from outflank_stage1.services.implant_service import ImplantService

ImplantService().get_by_uid(uid)        # -> Implant
ImplantService().get_all_implants()     # -> List[Implant]
```

### ChannelService

```python
from outflank_stage1.services.channel_service import ChannelService
from outflank_stage1.channel.enums import ChannelType

ChannelService.list()                                          # -> List[Channel]
ChannelService.create_channel(implant_uid, channel_type,       # -> Channel
    local_host=None, local_port=None,
    remote_host=None, remote_port=None)
ChannelService.delete_channel(channel_uid)
```

`ChannelType` values: `PORT_FORWARD`, `REV_PORT_FORWARD`, `LINK`, `SOCKS`.

`Channel` fields: `get_uid()`, `implant_uid`, `type`, `local_host`, `local_port`, `remote_host`, `remote_port`, `created`.

## Tasks

Typed tasks are exported from `outflank_stage1.task.tasks`. Many accept constructor values, for example:

```python
SleepTask(interval=60, jitter=30)
NoteTask(note_text="reviewed")
LsTask(path=r"C:\Users")
ExitTask()                          # or ExitTask(process=True)
```

Available typed task classes: `BurnTask`, `CatTask`, `CdTask`, `CheckTCCTask`, `ConfigTask`, `CpTask`, `DelayTask`, `DNSNameTask`, `DomainNameTask`, `DownloadTask`, `DrivesTask`, `EnvTask`, `ExecBOFTask`, `ExecBOFAsyncTask`, `ExecCommandTask`, `ExecDotnetTask`, `ExecJXATask`, `ExecProcessTask`, `ExecShellcodeTask`, `ExitTask`, `FullCheckinTask`, `GetPrivsTask`, `GetSystemTask`, `HelpTask`, `HooksTask`, `IPTask`, `TaskTask`, `KillTask`, `LinkTask`, `ListAppsTask`, `ListEntitlementsTask`, `LoadLibraryTask`, `LsTask`, `MakeTokenTask`, `MkdirTask`, `MvTask`, `NoteTask`, `PlistTask`, `PortforwardTask`, `PsTask`, `PsGrepTask`, `PsxTask`, `PsxxTask`, `PwdTask`, `RegTask`, `Rev2SelfTask`, `RmTask`, `RmdirTask`, `RPortForwardTask`, `ScreenshotTask`, `SocksTask`, `SleepTask`, `SpawnasTask`, `StealTokenTask`, `TimestompTask`, `UnlinkTask`, `UploadTask`, `UptimeTask`, `WhoamiTask`.

For an untyped server command:

```python
from outflank_stage1.task import GenericTask

task = GenericTask("windowlist")
task.set_arguments("optional arguments")
```

## Implant Accessors

`from outflank_stage1.implant import Implant`

| Method | Return type |
|---|---|
| `get_uid()` | `str` |
| `get_parent_uid()` | `Optional[str]` |
| `get_version()` | `Optional[str]` |
| `get_comm_type()` | `ImplantCommType` |
| `get_recipe()` | `Optional[str]` |
| `get_delay()` | `Optional[int]` |
| `get_jitter()` | `Optional[int]` |
| `get_kill_date()` | `Optional[datetime]` |
| `get_arch()` | `ImplantArch` |
| `get_os()` | `Optional[str]` |
| `get_os_type()` | `ImplantOSType` |
| `get_pid()` | `Optional[int]` |
| `get_ppid()` | `Optional[int]` |
| `get_privilege()` | `ImplantPrivilege` |
| `get_proc_name()` | `Optional[str]` |
| `get_pproc_name()` | `Optional[str]` |
| `get_hostname()` | `Optional[str]` |
| `get_username()` | `Optional[str]` |
| `get_token_impersonated()` | `bool` |
| `get_ip()` | `Optional[str]` |
| `get_transport_ip()` | `Optional[str]` |
| `get_note()` | `Optional[str]` |
| `get_first_seen()` | `Optional[datetime]` |
| `get_last_seen()` | `Optional[datetime]` |
| `get_checkin_count()` | `Optional[int]` |
| `get_visible()` | `bool` |
| `get_options()` | `int` |
| `get_tasks()` | `List[BaseTask]` |

Enum values from `outflank_stage1.implant.enums`:

- `ImplantArch`: `UNKNOWN`, `INTEL_X86`, `INTEL_X64`, `ARM64`
- `ImplantOSType`: `UNKNOWN`, `WINDOWS`, `MAC_OS`, `LINUX`, `FREEBSD`
- `ImplantPrivilege`: `UNKNOWN`, `UNTRUSTED`, `LOW`, `MEDIUM`, `HIGH`, `SYSTEM`, `PROTECTED_PROCESS`
- `ImplantCommType`: `UNKNOWN`, `HTTP_HTTPS`, `TCP`, `NAMEDPIPE`, `FILE_DISK`

## BaseTask Accessors

`from outflank_stage1.task import BaseTask`

| Method | Return type |
|---|---|
| `get_uid()` | `Optional[str]` |
| `get_name()` | `str` |
| `get_arguments()` | `Optional[str]` |
| `get_response()` | `Optional[str]` |
| `get_response_timestamp()` | `Optional[datetime]` |
| `get_response_bytes_total()` | `Optional[int]` |
| `get_state()` | `TaskState` |
| `get_timestamp()` | `Optional[datetime]` |
| `get_operator()` | `Optional[str]` |
| `get_implant_uid()` | `Optional[str]` |
| `get_implant()` | `Optional[Implant]` |
| `set_arguments(str)` | `BaseTask` |

`TaskState` values from `outflank_stage1.task.enums`: `UNKNOWN`, `WAITING`, `DISTRIBUTED`, `RUNNING`, `FINISHED`, `ERROR`.

Many model values are optional; check for `None` before using them.
