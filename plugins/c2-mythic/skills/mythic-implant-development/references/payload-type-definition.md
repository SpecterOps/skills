# Payload Type Definition

This page describes how to define a Mythic payload type, its build parameters, build function, and lifecycle hooks.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/payload-type-info/payload-type-definition

## PayloadType Class (Python)

```python
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
import json
import pathlib

class MyAgent(PayloadType):
    name = "myagent"
    file_extension = "bin"
    agent_type = AgentType.Agent
    author = "@yourhandle"
    mythic_encrypts = True
    supported_os = [
        SupportedOS.Windows,
        SupportedOS.Linux,
        SupportedOS.MacOS,
    ]
    semver = "1.0.0"
    note = "Description of your agent."
    supports_dynamic_loading = True
    supports_multiple_c2_instances_in_build = False
    supports_multiple_c2_in_build = False
    c2_profiles = ["http", "websocket"]
    agent_path = pathlib.Path(".") / "myagent" / "mythic"
    agent_code_path = pathlib.Path(".") / "myagent" / "agent_code"
    agent_icon_path = agent_path / "agent_functions" / "myagent.svg"

    build_parameters = [
        BuildParameter(
            name="output_type",
            parameter_type=BuildParameterType.ChooseOne,
            choices=["exe", "dll", "shellcode"],
            default_value="exe",
            description="Output format",
        ),
        BuildParameter(
            name="debug",
            parameter_type=BuildParameterType.Boolean,
            default_value=False,
            description="Debug build (DO NOT USE IN PRODUCTION)",
        ),
    ]

    build_steps = [
        BuildStep(step_name="Configuring", step_description="Stamping configuration values"),
        BuildStep(step_name="Compiling", step_description="Building the agent"),
    ]

    async def build(self) -> BuildResponse:
        resp = BuildResponse(status=BuildStatus.Success)
        # Build logic here
        return resp
```

## PayloadType Struct (GoLang)

```go
package agentfunctions

import (
    agentstructs "github.com/MythicMeta/MythicContainer/agent_structs"
)

var payloadDefinition = agentstructs.PayloadType{
    Name:                                   "myagent",
    FileExtension:                          "bin",
    Author:                                 "@yourhandle",
    SupportedOS:                            []string{
        agentstructs.SUPPORTED_OS_LINUX,
        agentstructs.SUPPORTED_OS_MACOS,
        agentstructs.SUPPORTED_OS_WINDOWS,
    },
    Wrapper:                                false,
    SupportsDynamicLoading:                 false,
    Description:                            "Description of your agent",
    SupportedC2Profiles:                    []string{"http", "websocket"},
    MythicEncryptsData:                     true,
    BuildParameters: []agentstructs.BuildParameter{
        {
            Name:          "mode",
            Description:   "Build mode",
            Required:      false,
            DefaultValue:  "default",
            Choices:       []string{"default", "c-shared"},
            ParameterType: agentstructs.BUILD_PARAMETER_TYPE_CHOOSE_ONE,
        },
    },
    BuildSteps: []agentstructs.BuildStep{
        {
            Name:        "Configuring",
            Description: "Stamping configuration values",
        },
        {
            Name:        "Compiling",
            Description: "Building the agent binary",
        },
    },
}

func build(payloadBuildMsg agentstructs.PayloadBuildMessage) agentstructs.PayloadBuildResponse {
    payloadBuildResponse := agentstructs.PayloadBuildResponse{
        PayloadUUID:        payloadBuildMsg.PayloadUUID,
        Success:            true,
        UpdatedCommandList: &payloadBuildMsg.CommandList,
    }
    return payloadBuildResponse
}

func Initialize() {
    agentstructs.AllPayloadData.Get("myagent").AddPayloadDefinition(payloadDefinition)
    agentstructs.AllPayloadData.Get("myagent").AddBuildFunction(build)
    agentstructs.AllPayloadData.Get("myagent").AddIcon(filepath.Join(".", "myagent", "agentfunctions", "myagent.svg"))
}
```

## Key Fields

| Field (Python) | Field (Go) | Description |
|----------------|------------|-------------|
| `name` | `Name` | Agent name (lowercase, no capitals - Docker limitation) |
| `file_extension` | `FileExtension` | Default file extension for built payloads |
| `agent_type` | `Wrapper` (bool) | `AgentType.Agent` for normal agents, `AgentType.Wrapper` for wrappers |
| `mythic_encrypts` | `MythicEncryptsData` | If `True`, Mythic handles encryption. If `False`, you must use a translation container. |
| `supported_os` | `SupportedOS` | Array of OS the agent supports |
| `supports_dynamic_loading` | `SupportsDynamicLoading` | If `True`, operators can select a subset of commands when building |
| `c2_profiles` | `SupportedC2Profiles` | Array of C2 profile names the agent supports |
| `agent_path` | N/A | Path to the mythic definition code |
| `agent_code_path` | N/A | Path to the agent source code |
| `translation_container` | N/A | Name of translation container (if using custom message format) |

**IMPORTANT**: In Python the field is `c2_profiles` (NOT `supported_c2_profiles`). The Go struct uses `SupportedC2Profiles` but these are different languages with different naming. Do not confuse the two.

## BuildParameter Types

| Type | Value at Build Time |
|------|-------------------|
| `BuildParameterType.String` | string |
| `BuildParameterType.Boolean` | boolean |
| `BuildParameterType.ChooseOne` | string |
| `BuildParameterType.ChooseMultiple` | list[str] |
| `BuildParameterType.Array` | list[str] |
| `BuildParameterType.Date` | string "YYYY-MM-DD" |
| `BuildParameterType.Dictionary` | dict |
| `BuildParameterType.File` | string (file UUID) |
| `BuildParameterType.TypedArray` | list[list] |

### BuildParameter Attributes

| Attribute | Description |
|-----------|-------------|
| `name` | Parameter name |
| `description` | Shown to operator |
| `parameter_type` | One of the types above |
| `default_value` | Default if operator doesn't set one |
| `required` | Must have a non-empty value |
| `choices` | Options for ChooseOne/ChooseMultiple |
| `randomize` | Randomize value per payload build |
| `format_string` | Regex format for randomization |
| `crypto_type` | If `True`, generates enc_key/dec_key |
| `verifier_regex` | UI validation regex |
| `group_name` | Group related parameters in UI |
| `supported_os` | Only show for certain OS selections |
| `hide_conditions` | Conditionally hide based on other parameter values |

## Build Function

### Available Context (Python)

| Property | Description |
|----------|-------------|
| `self.uuid` | Payload UUID (agent identifies itself with this before getting a callback UUID) |
| `self.commands.get_commands()` | List of selected command names |
| `self.agent_code_path` | Path to agent source code directory |
| `self.get_parameter("name")` | Get build parameter value |
| `self.selected_os` | OS selected by operator |
| `self.c2info` | List of C2 profile configurations |

### Available Context (GoLang)

The `PayloadBuildMessage` struct provides:

```go
type PayloadBuildMessage struct {
    PayloadType     string
    Filename        string
    CommandList     []string
    BuildParameters PayloadBuildArguments
    C2Profiles      []PayloadBuildC2Profile
    WrappedPayload  *[]byte
    SelectedOS      string
    PayloadUUID     string
    PayloadFileUUID string
}
```

### Accessing C2 Parameters (Python)

```python
for c2 in self.c2info:
    profile = c2.get_c2profile()   # {"name": "http", "description": "...", "is_p2p": false}
    params = c2.get_parameters_dict()  # {"callback_host": "https://...", "AESPSK": {...}, ...}

    for key, val in params.items():
        if key == "AESPSK":
            enc_key = val["enc_key"]  # base64 string or None
            dec_key = val["dec_key"]  # base64 string or None
        elif isinstance(val, dict):
            # Dictionary parameter (e.g., headers)
            pass
        else:
            # String/number parameter
            pass
```

### BuildResponse

| Field | Description |
|-------|-------------|
| `status` | `BuildStatus.Success` or `BuildStatus.Error` |
| `payload` | Raw bytes of the built payload (empty on error) |
| `build_message` | Message shown to operator |
| `build_stderr` | stderr output |
| `build_stdout` | stdout output |
| `updated_filename` | Override the filename (e.g., change `.exe` to `.dll`) |
| `updated_command_list` | Adjust which commands are included |

### Build Steps Updates (Python)

```python
await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
    PayloadUUID=self.uuid,
    StepName="Compiling",
    StepStdout="compilation output...",
    StepSuccess=True,
))
```

### Build Environment Constraints

**CRITICAL**: The `build` function executes inside the payload type's Docker container. This means:

- You **CANNOT** use `docker` commands (Docker is not available inside the container)
- You **CANNOT** access the host filesystem outside of `/Mythic/`
- You CAN only use tools that are installed in the container's Dockerfile
- All compilation, linking, and packaging must use tools available inside the container
- Common tools available: compilers installed via `RUN apt-get install` or `RUN pip install` in the Dockerfile, plus whatever the base image provides (Go, Python, .NET, etc.)

For example, if your agent is written in Rust, you must install the Rust toolchain in the Dockerfile (`RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y`), then call `cargo build` via `subprocess` or `os.exec` in your build function. You cannot use Docker-in-Docker.

### Temporary Build Directory

If the build modifies files, work in a temp copy:

```python
import tempfile
from distutils.dir_util import copy_tree

agent_build_path = tempfile.TemporaryDirectory(suffix=self.uuid)
copy_tree(str(self.agent_code_path), agent_build_path.name)
# Work in agent_build_path.name
```

## On New Callback

Optional function called when a new callback registers. Can automatically issue tasking.

### Python

```python
async def on_new_callback(self, newCallback: PTOnNewCallbackAllData) -> PTOnNewCallbackResponse:
    new_task_resp = await SendMythicRPCTaskCreate(MythicRPCTaskCreateMessage(
        AgentCallbackUUID=newCallback.Callback.AgentCallbackID,
        CommandName="shell",
        Params="whoami",
    ))
    return PTOnNewCallbackResponse(
        AgentCallbackUUID=newCallback.Callback.AgentCallbackID,
        Success=new_task_resp.Success,
    )
```

### GoLang

```go
func onNewCallback(data agentstructs.PTOnNewCallbackAllData) agentstructs.PTOnNewCallbackResponse {
    newTasking, _ := mythicrpc.SendMythicRPCTaskCreate(mythicrpc.MythicRPCTaskCreateMessage{
        AgentCallbackID: data.Callback.AgentCallbackID,
        CommandName:     "shell",
        Params:          "whoami",
    })
    return agentstructs.PTOnNewCallbackResponse{
        AgentCallbackID: data.Callback.AgentCallbackID,
        Success:         true,
    }
}

// Register in Initialize():
agentstructs.AllPayloadData.Get("myagent").AddOnNewCallbackFunction(onNewCallback)
```

Mythic associates auto-created tasks with the operator who built the payload.

## Wrapper Payload Types

Wrappers take another payload's output and repackage it:

- Set `agent_type = AgentType.Wrapper` (Python) or `Wrapper: true` (Go)
- No C2 profiles (wrappers don't have their own comms)
- Access wrapped payload via `self.wrapped_payload` (Python, base64) or `payloadBuildMsg.WrappedPayload` (Go, raw bytes)

Example: a service wrapper takes shellcode and wraps it in a Windows service executable.

## C2 Parameter Deviations

Override C2 profile parameters for agent-specific restrictions:

```python
c2_parameter_deviations = {
    "http": {
        "get_uri": C2ParameterDeviation(supported=False),
        "query_path_name": C2ParameterDeviation(supported=False),
    }
}
```

## CustomRPCFunctions

Expose RPC functions callable from other containers:

```python
custom_rpc_functions = {
    "my_function": my_function_handler
}
```

Other containers call these via `PTOtherServiceRPCMessage` with the service name, function name, and arguments.
