# Create Tasking

This page describes the `create_go_tasking` function for server-side task preprocessing, available context, and RPC functionality.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking

## create_go_tasking Function

Every command must implement this function. It runs after argument parsing and before the task is available to the agent.

### Python

```python
async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
    response = PTTaskCreateTaskingMessageResponse(
        TaskID=taskData.Task.ID,
        Success=True,
    )
    return response
```

### GoLang

```go
TaskFunctionCreateTasking: func(taskData *agentstructs.PTTaskMessageAllData) agentstructs.PTTaskCreateTaskingMessageResponse {
    response := agentstructs.PTTaskCreateTaskingMessageResponse{
        Success: true,
        TaskID:  taskData.Task.ID,
    }
    return response
},
```

## Available Context

### taskData.Task

Information about the issued task (ID, operator, original params, status, etc.)

### taskData.Callback

Information about the callback (hostname, user, PID, integrity level, domain, OS, etc.)

### taskData.Payload

Information about the backing payload (UUID, build parameters, etc.)

### taskData.Commands

List of commands currently loaded into this callback.

### taskData.BuildParameters

Build parameter names and values used when creating the payload.

### taskData.C2Profiles

C2 profile information and parameters for this callback.

### taskData.args

Access to parsed and validated command arguments:

```python
# Get a parameter value
value = taskData.args.get_arg("remote_path")

# Set/update a parameter value
taskData.args.add_arg("remote_path", "/new/path")

# Set with a different type
taskData.args.add_arg("count", 5, ParameterType.Number)

# Add a new parameter for this task only
taskData.args.add_arg("new_key", "new_value")

# Remove a parameter
taskData.args.remove_arg("key")

# Rename a parameter
taskData.args.rename_arg("old_key", "new_key")

# Check if parameter exists
if taskData.args.has_arg("key"):
    pass

# Access raw command line
raw = taskData.args.commandline
```

**Important**: When adding args with multiple parameter groups, specify which group the new arg belongs to. By default it's added to "Default" which may not match the active group.

### taskData.Task.TokenID

Token ID used with the task (requires the callback to have reported tokens). 0 if no token.

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `Success` | bool | Did processing succeed |
| `Error` | string | Error message if `Success=False` |
| `TaskID` | int | Task ID (always set from `taskData.Task.ID`) |
| `CommandName` | string | Override the command name the agent sees (for aliases) |
| `TaskStatus` | string | Override task status. `"error: ..."` renders red in UI. |
| `DisplayParams` | string | Human-readable params shown in UI instead of raw JSON |
| `Stdout` | string | Additional stdout (visible in task details, not main output) |
| `Stderr` | string | Additional stderr (visible in task details) |
| `Completed` | bool | If `True`, mark task done immediately (agent won't pick it up) |
| `CompletionFunctionName` | string | Function to call when task completes |
| `ParameterGroupName` | string | Override the determined parameter group |

### DisplayParams

Useful for showing operator-friendly text instead of JSON blobs:

```python
response.DisplayParams = f"uploading {filename} to {remote_path}"
```

### CompletionFunctionName

Register a function to run when the task completes:

```python
# In command definition:
completion_functions = {"formulate_output": formulate_output}

# In create_go_tasking:
response.CompletionFunctionName = "formulate_output"
```

### CommandName Override (Aliases)

Create a `script_only` command that aliases another command:

```python
class DirCommand(CommandBase):
    cmd = "dir"
    script_only = True
    # ...

    async def create_go_tasking(self, taskData):
        response = PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID, Success=True,
        )
        response.CommandName = "ls"  # Agent sees "ls" instead of "dir"
        return response
```

## RPC Functionality

From `create_go_tasking` you can make RPC calls to Mythic. All follow the pattern:

```python
result = await SendMythicRPC*(MythicRPC*Message(...))
```

### Common RPC Calls

**Create artifacts:**
```python
await SendMythicRPCArtifactCreate(MythicRPCArtifactCreateMessage(
    TaskID=taskData.Task.ID,
    ArtifactMessage=f"{taskData.args.get_arg('command')}",
    BaseArtifactType="Process Create"
))
```

**Get file contents:**
```python
file_resp = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
    AgentFileId=taskData.args.get_arg("file"),
))
```

**Search files:**
```python
file_resp = await SendMythicRPCFileSearch(MythicRPCFileSearchMessage(
    TaskID=taskData.Task.ID,
    AgentFileID=taskData.args.get_arg("file")
))
```

**Create a new file:**
```python
await SendMythicRPCFileCreate(MythicRPCFileCreateMessage(...))
```

**Update file metadata:**
```python
await SendMythicRPCFileUpdate(MythicRPCFileUpdateMessage(...))
```

**Create sub-tasks:**
```python
await SendMythicRPCTaskCreate(MythicRPCTaskCreateMessage(
    AgentCallbackUUID=taskData.Callback.AgentCallbackID,
    CommandName="shell",
    Params="whoami",
))
```

**Update build steps:**
```python
await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
    PayloadUUID=self.uuid,
    StepName="Compiling",
    StepSuccess=True,
))
```

**Create responses:**
```python
await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
    TaskID=taskData.Task.ID,
    Response="output text for operator",
))
```

## Execution Flow

1. Operator submits task (UI, CLI, or scripting)
2. Mythic stores task in database
3. TaskArguments instantiated and parsed
4. Parameter group determined, defaults applied, validation run
5. `opsec_pre` called (if defined)
6. `create_go_tasking` called
7. `opsec_post` called (if defined)
8. Task enters "Submitted" state for agent pickup

If any step fails or is blocked, the task does not advance to the next step.
