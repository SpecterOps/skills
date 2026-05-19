# Post Response (Submitting Task Results)

This page describes how an agent submits task output to Mythic.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/action-post_response

## Key Difference from get_tasking

- `post_response` with `responses`: returns acknowledgment but **no new tasks**
- `get_tasking` with `responses`: returns acknowledgment **plus** new tasks

If you want to combine task output with fetching new work, include `responses` in your `get_tasking` message instead.

## Request: Agent -> Mythic

```json
Base64( CallbackUUID + EncBlob(
    JSON({
        "action": "post_response",
        "responses": [
            {
                "task_id": "uuid of task",
                // ... response fields (see below)
            },
            {
                "task_id": "uuid of another task",
                // ... response fields
            }
        ],

        // optional - P2P forwarding
        "delegates": [
            {"message": "<agentMessage>", "c2_profile": "ProfileName", "uuid": "uuid here"}
        ]
    })
)
)
```

## Response Fields

Each entry in the `responses` array must have `task_id` plus any combination of the following:

### Basic Output

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | **Required** - UUID of the task this response is for |
| `user_output` | string | Text output displayed directly to the operator |
| `completed` | boolean | `true` marks the task as finished |
| `status` | string | Task status. Use `"success"` for success. Prefix with `"error: "` for red text in UI. Any other value appears as blue text. |

Minimal response example:
```json
{
    "task_id": "uuid-here",
    "user_output": "command completed successfully",
    "completed": true,
    "status": "success"
}
```

Error response example:
```json
{
    "task_id": "uuid-here",
    "user_output": "detailed error message for operator",
    "completed": true,
    "status": "error: authentication failed"
}
```

### process_response

Instead of `user_output` (which goes directly to the operator), use `process_response` to route output through the command's `process_response` function in the Mythic container. This enables server-side processing with MythicRPC (register files, credentials, etc.) before displaying results.

```json
{
    "task_id": "uuid-here",
    "process_response": "{\"some\": \"structured data\"}"
}
```

### Additional Response Fields

The `responses` array entries can also include structured data for Mythic features. These are covered in detail in the file download/upload references and the Mythic hooking features documentation:

- `download` - File download registration and chunks
- `upload` - File upload chunk requests
- `artifacts` - Artifact tracking
- `credentials` - Credential reporting
- `edges` - P2P connection updates
- `file_browser` - File browser data
- `process_response` - Server-side processing
- `removed_files` - File removal tracking
- `keylogs` - Keystroke data

## Response: Mythic -> Agent

```json
Base64( CallbackUUID + EncBlob(
    JSON({
        "action": "post_response",
        "responses": [
            {
                "task_id": "UUID",
                "status": "success",
                "error": "error message if status is error"
            }
        ],

        "delegates": [
            {"message": "<agentMessage>", "c2_profile": "ProfileName", "uuid": "uuid here"}
        ]
    })
)
)
```

**Note**: If the agent's `responses` array was improperly formatted (Mythic couldn't deserialize it), the response `responses` array will be empty - no `task_id` entries. This means you cannot always match response entries 1:1 with sent entries.

## Additional Fields in post_response

Like `get_tasking`, the `post_response` message can also carry:

- `socks` - SOCKS5 proxy data. Array of `{exit, server_id, data}` messages. See [SOCKS](./socks.md).
- `rpfwd` - Reverse port forward data. Array of `{exit, server_id, data, port}` messages. See [Reverse Port Forward](./rpfwd.md).
- `interactive` - Interactive tasking data
- `alerts` - Alert messages
- `edges` - P2P connection updates
- `delegates` - P2P forwarded messages

The difference from `get_tasking` is that you will NOT receive a `tasks` array back - only acknowledgments and delegate responses.

**Important**: Mythic may include `socks` and/or `rpfwd` arrays in its response to ANY `post_response` message. The agent must always check for these.
