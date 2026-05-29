# Commands

This page describes how to define commands, their arguments, and parameter types for a Mythic agent.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/adding-commands/commands

## Command Architecture

Each command has two parts:
- **CommandBase** (Python) / Command struct (Go) - metadata and server-side functions
- **TaskArguments** (Python) / argument parsing (Go) - parameter definitions and validation

## CommandBase (Python)

```python
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *

class ShellCommand(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell {command}"
    description = "Execute a shell command"
    version = 1
    author = "@author"
    attackmapping = ["T1059", "T1059.004"]
    argument_class = ShellArguments
    attributes = CommandAttributes(
        spawn_and_injectable=True,
        supported_os=[SupportedOS.Windows, SupportedOS.Linux],
        builtin=False,
        load_only=False,
        suggested_command=True,
    )
    script_only = False

    async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
        response = PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID, Success=True,
        )
        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
```

### CommandBase Fields

| Field | Type | Description |
|-------|------|-------------|
| `cmd` | string | Command name (used for lookup, not the class name) |
| `needs_admin` | bool | Whether admin permissions are required |
| `help_cmd` | string | Help text shown with `help <command>` |
| `description` | string | Command description |
| `version` | int | Command version for tracking changes |
| `author` | string | Command author |
| `attackmapping` | list[str] | MITRE ATT&CK technique IDs (e.g., `["T1059"]`) |
| `argument_class` | class | Reference to the TaskArguments subclass |
| `script_only` | bool | If `True`, task never reaches the agent - only runs server-side `create_go_tasking` |

### CommandAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `supported_os` | list | OS filter: `[SupportedOS.Windows, SupportedOS.MacOS, SupportedOS.Linux]` |
| `spawn_and_injectable` | bool | Whether the command can be injected into another process |
| `builtin` | bool | Always included in builds, cannot be deselected |
| `load_only` | bool | Cannot be built-in, only loaded at runtime |
| `suggested_command` | bool | Pre-selected when building a payload |
| `filter_by_build_parameter` | dict | Filter command availability by build parameter values |

Custom attributes can be added as key=value pairs and retrieved via RPC (useful for dependency tracking in `load` commands).

### supported_ui_features

Array of UI integration points:

```python
supported_ui_features = ["callback_table:exit"]      # Exit button in callback table
supported_ui_features = ["file_browser:list"]         # List in file browser
supported_ui_features = ["file_browser:download"]     # Download from file browser
supported_ui_features = ["file_browser:upload"]       # Upload from file browser
supported_ui_features = ["file_browser:remove"]       # Remove from file browser
supported_ui_features = ["process_browser:list"]      # Process browser list
supported_ui_features = ["task_response:interactive"]  # Interactive tasking
```

## TaskArguments (Python)

```python
class ShellArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="command",
                type=ParameterType.String,
                description="Command to execute",
                parameter_group_info=[ParameterGroupInfo(required=True)]
            )
        ]

    async def parse_arguments(self):
        if len(self.command_line) == 0:
            raise ValueError("Must supply a command")
        self.add_arg("command", self.command_line)

    async def parse_dictionary(self, dictionary_arguments):
        self.load_args_from_dictionary(dictionary_arguments)
```

### TaskArguments Context

Within your TaskArguments subclass:

| Property | Description |
|----------|-------------|
| `self.command_line` | Parameters string to parse |
| `self.raw_command_line` | Original unprocessed user input |
| `self.tasking_location` | Source: `command_line`, `parsed_cli`, `modal`, `browserscript` |
| `self.task_dictionary` | Dict with task metadata (parameter_group_name, user, etc.) |
| `self.parameter_group_name` | Override to manually set the parameter group |

### parse_arguments vs parse_dictionary

- `parse_arguments` - REQUIRED. Called for all input. Handles free-form string parsing.
- `parse_dictionary` - OPTIONAL. Called when input is already a dictionary (from modal, parsed CLI, or browserscript). Simpler than string parsing.

```python
async def parse_arguments(self):
    if len(self.command_line) == 0:
        raise ValueError("Must supply arguments")
    if self.command_line[0] == "{":
        self.load_args_from_json_string(self.command_line)
        return
    # Parse free-form text
    pieces = self.command_line.split(" ")
    self.add_arg("arg1", pieces[0])
    self.add_arg("arg2", pieces[1])

async def parse_dictionary(self, dictionary_arguments):
    self.load_args_from_dictionary(dictionary_arguments)
```

## CommandParameter

```python
CommandParameter(
    name="path",                           # Internal name (used in agent)
    display_name="File Path",              # Shown in modal (optional)
    cli_name="path",                       # Used on command line -path (optional)
    type=ParameterType.String,
    description="Path to the file",
    default_value=".",
    required=True,
    choices=["opt1", "opt2"],              # For ChooseOne/ChooseMultiple
    validation_func=my_validator,          # Custom validation function
    dynamic_query_function=my_query,       # Dynamic choices via RPC
    parameter_group_info=[ParameterGroupInfo(
        group_name="Default",
        required=True,
        ui_position=1
    )]
)
```

### Parameter Types

| Type | Value in Agent | Description |
|------|---------------|-------------|
| `ParameterType.String` | string | Free text |
| `ParameterType.Boolean` | boolean | True/False toggle |
| `ParameterType.Number` | number | Numeric value |
| `ParameterType.ChooseOne` | string | Select one from choices |
| `ParameterType.ChooseOneCustom` | string | Select from choices OR type custom |
| `ParameterType.ChooseMultiple` | list[str] | Select multiple from choices |
| `ParameterType.Array` | list[str] | Array of strings |
| `ParameterType.TypedArray` | list[list] | Array of [type, value] pairs (useful for BOF args) |
| `ParameterType.File` | string (UUID) | File upload - agent gets UUID, use RPC to get contents |
| `ParameterType.Date` | string | Date in YYYY-MM-DD format |
| `ParameterType.Dictionary` | dict | Key-value pairs |
| `ParameterType.Credential_JSON` | dict | Select from Mythic credential store |
| `ParameterType.Payload` | string (UUID) | Select an existing payload |
| `ParameterType.ConnectionInfo` | dict | P2P connection target selection |
| `ParameterType.LinkInfo` | dict | Active/dead P2P connection selection |

### Parameter Groups

Parameters can belong to multiple groups for conditional display:

```python
self.args = [
    CommandParameter(
        name="file",
        type=ParameterType.File,
        description="Upload a new file",
        parameter_group_info=[
            ParameterGroupInfo(required=True, group_name="Default")
        ]
    ),
    CommandParameter(
        name="filename",
        type=ParameterType.ChooseOne,
        description="Select existing file",
        dynamic_query_function=self.get_files,
        parameter_group_info=[
            ParameterGroupInfo(required=True, group_name="existing_file")
        ]
    ),
    CommandParameter(
        name="remote_path",
        type=ParameterType.String,
        description="Destination path on target",
        parameter_group_info=[
            ParameterGroupInfo(required=True, group_name="Default", ui_position=1),
            ParameterGroupInfo(required=True, group_name="existing_file", ui_position=1),
        ]
    ),
]
```

Here `file` and `filename` are mutually exclusive (different groups), while `remote_path` appears in both groups.

### Dynamic Query Functions

For ChooseOne/ChooseMultiple with dynamic choices:

```python
async def get_files(self, inputMsg: PTRPCDynamicQueryFunctionMessage) -> PTRPCDynamicQueryFunctionMessageResponse:
    fileResponse = PTRPCDynamicQueryFunctionMessageResponse(Success=False)
    file_resp = await MythicRPC().execute("get_file",
        callback_id=inputMsg.Callback,
        limit_by_callback=False,
        filename="",
        max_results=-1)
    if file_resp.status == MythicRPCStatus.Success:
        file_names = []
        for f in file_resp.response:
            if f["filename"] not in file_names:
                file_names.append(f["filename"])
        fileResponse.Success = True
        fileResponse.Choices = file_names
    return fileResponse
```

## Processing Order

1. Task stored in database
2. TaskArguments instantiated with parameters
3. `parse_dictionary` or `parse_arguments` called
4. Parameter group determined from set parameters
5. Default values applied to unset non-required parameters
6. Required parameters validated
7. `opsec_pre` called
8. `create_go_tasking` called
9. `opsec_post` called
10. Task enters `Submitted` state (or `Completed` if `script_only=True`)
