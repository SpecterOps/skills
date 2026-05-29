# OPSEC Checking

This page describes the `opsec_pre` and `opsec_post` functions for gating tasks on operational security checks.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/opsec-checking

## Overview

OPSEC checks allow you to block or warn about tasks based on security concerns before the agent picks them up. This is more granular than blanket command blocking from the Operation Management page.

Two check points:
- **opsec_pre** - runs BEFORE `create_go_tasking`
- **opsec_post** - runs AFTER `create_go_tasking` (after artifacts are generated)

## opsec_pre (Python)

```python
async def opsec_pre(self, taskData: PTTaskMessageAllData) -> PTTTaskOPSECPreTaskMessageResponse:
    response = PTTTaskOPSECPreTaskMessageResponse(
        TaskID=taskData.Task.ID,
        Success=True,
        OpsecPreBlocked=True,
        OpsecPreBypassRole="other_operator",
        OpsecPreMessage="This command spawns a child process visible to EDR.",
    )
    return response
```

## opsec_post (Python)

```python
async def opsec_post(self, taskData: PTTaskMessageAllData) -> PTTTaskOPSECPostTaskMessageResponse:
    response = PTTTaskOPSECPostTaskMessageResponse(
        TaskID=taskData.Task.ID,
        Success=True,
        OpsecPostBlocked=True,
        OpsecPostBypassRole="lead",
        OpsecPostMessage="This task writes a detectable artifact to disk.",
    )
    return response
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `OpsecPre/PostBlocked` | bool | `True` to block the task, `False` to allow |
| `OpsecPre/PostMessage` | string | Message explaining why the task was blocked/flagged |
| `OpsecPre/PostBypassRole` | string | Who can bypass the block |

### Bypass Roles

| Role | Who Can Bypass |
|------|----------------|
| `"operator"` | Any operator (default) |
| `"lead"` | Only the operation lead |
| `"other_operator"` | Any operator OTHER THAN the one who issued the task |

`other_operator` is useful for checks that aren't blocking but need acknowledgment - forces a second pair of eyes.

## Execution Order

```
Task Submitted
    │
    ▼
opsec_pre ──── Blocked? ──── Yes ──── Wait for bypass
    │                                       │
    │ (not blocked or bypassed)             │
    ▼                                       ▼
create_go_tasking ◄─────────────────────────┘
    │
    ▼
opsec_post ──── Blocked? ──── Yes ──── Wait for bypass
    │                                       │
    │ (not blocked or bypassed)             │
    ▼                                       ▼
Task Status: "Submitted" ◄─────────────────┘
(agent can pick up)
```

If `opsec_pre` blocks: `create_go_tasking` does NOT run until bypass.
If `opsec_post` blocks: task does NOT enter "Submitted" until bypass.

## Available Context

Both functions have access to:
- Full task/callback information (same as `create_go_tasking`)
- The full RPC suite (MythicRPC calls)
- Parsed command arguments

## Example: Shell Command with OPSEC Checks

```python
class ShellCommand(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell {command}"
    description = "Execute a shell command. WARNING: spawns a child process."
    version = 1
    attackmapping = ["T1059", "T1059.004"]
    argument_class = ShellArguments

    async def opsec_pre(self, taskData: PTTaskMessageAllData) -> PTTTaskOPSECPreTaskMessageResponse:
        response = PTTTaskOPSECPreTaskMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            OpsecPreBlocked=True,
            OpsecPreBypassRole="operator",
            OpsecPreMessage="shell spawns a child process - may trigger EDR behavioral detection.",
        )
        return response

    async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
        response = PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID, Success=True,
        )
        # Register artifact
        await SendMythicRPCArtifactCreate(MythicRPCArtifactCreateMessage(
            TaskID=taskData.Task.ID,
            ArtifactMessage=f"{taskData.args.get_arg('command')}",
            BaseArtifactType="Process Create"
        ))
        response.DisplayParams = taskData.args.get_arg("command")
        return response
```

## When to Use OPSEC Checks

Implement checks on commands that:
- Create new processes (shell, execute, spawn)
- Write files to disk (upload, drop)
- Make network connections (lateral movement, port scanning)
- Touch sensitive APIs (credential dumping, token manipulation)
- Create registry keys or scheduled tasks
- Inject into processes

The check should explain the risk and let the operator make an informed decision about whether to proceed.
