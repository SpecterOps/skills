# Get Tasking

This page describes the protocol for an agent to request pending tasks from Mythic.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/action_get_tasking

## Request: Agent -> Mythic

```json
Base64( CallbackUUID + EncBlob(
    JSON({
        "action": "get_tasking",
        "tasking_size": 1,

        // optional - forward P2P delegate messages
        "delegates": [
            {"message": "<agentMessage>", "c2_profile": "ProfileName", "uuid": "uuid here"}
        ],

        // optional - defaults to true
        "get_delegate_tasks": true
    })
)
)
```

### Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `action` | Yes | - | Must be `"get_tasking"` |
| `tasking_size` | No | 1 | Max number of tasks to return. Use `-1` for ALL pending tasks. |
| `delegates` | No | - | Array of P2P forwarded messages from linked agents |
| `get_delegate_tasks` | No | `true` | If `true`, also fetch tasks for agents reachable through this callback |

### About get_delegate_tasks

When set to `true` (default), if agentA has a route to agentB and agentB has a pending task, agentA's `get_tasking` will also pick up agentB's task. Set to `false` if your linked agents issue their own periodic `get_tasking` messages - prevents the parent from consuming a child's tasks.

## Response: Mythic -> Agent

```json
Base64( CallbackUUID + EncBlob(
    JSON({
        "action": "get_tasking",
        "tasks": [
            {
                "command": "command name",
                "parameters": "command param string",
                "timestamp": 1578706611.324671,
                "id": "task uuid"
            }
        ],

        // P2P responses for delegates in the request
        "delegates": [
            {"message": "<agentMessage>", "c2_profile": "ProfileName", "uuid": "uuid here"}
        ]
    })
)
)
```

### Fields

| Field | Description |
|-------|-------------|
| `tasks` | Array of 0 to `tasking_size` task objects |
| `tasks[].command` | The command name to execute |
| `tasks[].parameters` | String containing command parameters. If the command has structured parameters like `{"remote_path": "/tmp/file", "file_id": "uuid"}`, this will be a JSON string that the agent must parse. |
| `tasks[].timestamp` | Unix timestamp for ordering |
| `tasks[].id` | Task UUID - used when posting responses |
| `delegates` | Responses for any delegate messages sent in the request |

## Combining with Responses

The `get_tasking` request **CAN** also include these fields:

- `responses` - task output (same format as `post_response`)
- `socks` - SOCKS5 proxy data. Array of `{exit, server_id, data}` messages for tunneling TCP connections through the agent. See [SOCKS](./socks.md).
- `rpfwd` - Reverse port forward data. Array of `{exit, server_id, data, port}` messages for reverse-tunneling connections back through Mythic. See [Reverse Port Forward](./rpfwd.md).
- `edges` - P2P connection updates
- `alerts` - Alert messages
- `interactive` - Interactive tasking data

**Important**: Mythic may include `socks` and/or `rpfwd` arrays in its response to ANY `get_tasking` request. The agent must always check for and process these arrays, not just when it expects proxy traffic.

This allows the agent to send results AND request new tasking in a single message, avoiding two round-trips per sleep cycle.

Example combined message:

```json
{
    "action": "get_tasking",
    "tasking_size": -1,
    "responses": [
        {
            "task_id": "uuid-of-completed-task",
            "completed": true,
            "user_output": "command output here"
        }
    ]
}
```
