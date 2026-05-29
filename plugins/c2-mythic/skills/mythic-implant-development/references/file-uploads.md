# File Uploads (Mythic -> Agent)

This page describes how an agent pulls files from the Mythic server to the target.

Source: https://docs.mythic-c2.net/customizing/hooking-features/action-upload

## Overview

File uploads are agent-initiated pulls. The agent requests chunks from Mythic rather than Mythic pushing data. This allows the agent to control throughput and channel selection.

## How Files Get to Mythic

When an operator issues a command with a `File` type parameter:

1. Operator selects a file in the UI
2. Mythic uploads and stores the file, assigns a UUID
3. The command parameters contain the **file UUID**, not raw bytes
4. Example parameters sent to agent: `{"file": "uuid-here", "path": "/some/path"}`

## Server-Side: Accessing File Data in create_go_tasking

### Get File Contents (Python)

```python
async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
    response = PTTaskCreateTaskingMessageResponse(
        TaskID=taskData.Task.ID, Success=True,
    )
    file_resp = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=taskData.args.get_arg("file"),
    ))
    if file_resp.Success:
        # file_resp.Content contains raw bytes
        pass
    else:
        raise Exception("Error from Mythic: " + str(file_resp.error))
    return response
```

### Get File Metadata (Python)

```python
file_resp = await SendMythicRPCFileSearch(MythicRPCFileSearchMessage(
    TaskID=taskData.Task.ID,
    AgentFileID=taskData.args.get_arg("file")
))
if file_resp.Success and len(file_resp.Files) > 0:
    original_filename = file_resp.Files[0].Filename
```

### Swap File UUID for Contents

If your agent needs the raw file bytes in the tasking parameters (rather than pulling chunks):

```python
file_resp = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
    AgentFileId=taskData.args.get_arg("file"),
))
if file_resp.Success:
    import base64
    taskData.args.add_arg("file", base64.b64encode(file_resp.Content).decode())
```

### Register a New File

To register a file created by the container (not uploaded by the operator):

```python
await SendMythicRPCFileCreate(MythicRPCFileCreateMessage(...))
```

## Agent-Side: Chunked File Pull

The agent requests the file chunk by chunk:

### Request Each Chunk

```json
{
    "action": "post_response",
    "responses": [
        {
            "upload": {
                "chunk_size": 512000,
                "file_id": "UUID of the file",
                "chunk_num": 1,
                "full_path": "/full/path/on/target"
            },
            "task_id": "task uuid"
        }
    ]
}
```

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `chunk_size` | Yes | Bytes per chunk requested |
| `file_id` | Yes | UUID of the file to download |
| `chunk_num` | Yes | **1-based**. Which chunk to fetch. |
| `full_path` | Conditional | Full path where file will be written on target. Required for Mythic to track the file as written to disk. Omit if file stays in memory only. |
| `task_id` | Yes | Associated task UUID |

### Response from Mythic

```json
{
    "action": "post_response",
    "responses": [
        {
            "status": "success",
            "total_chunks": 4,
            "chunk_num": 1,
            "chunk_data": "base64 encoded chunk",
            "file_id": "file UUID",
            "task_id": "task UUID"
        }
    ]
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `total_chunks` | Total number of chunks given the requested `chunk_size` |
| `chunk_num` | Which chunk Mythic is returning |
| `chunk_data` | Base64-encoded file data |

The agent repeats the request for `chunk_num` 2 through `total_chunks`.

### Error Response

```json
{
    "action": "post_response",
    "responses": [
        {
            "total_chunks": 0,
            "chunk_num": 0,
            "chunk_data": "",
            "file_id": "",
            "task_id": "",
            "status": "error",
            "error": "error message"
        }
    ]
}
```

## full_path and Disk Tracking

- If `full_path` is provided: Mythic records the file as written to disk on the target, visible in the Files search page
- If `full_path` is empty or omitted: Mythic treats the transfer as memory-only (no disk artifact recorded)
- This is separate from artifact reporting on the Artifacts page

## File Reuse

Files can be pulled multiple times by default. If `delete_after_fetch` was set to `True` on the file, it will be removed from disk after the first complete fetch and cannot be re-used.

## Why Not Inline Files in Tasking?

Files are kept separate from tasking JSON to:
- Keep initial tasking messages small
- Allow the agent to use a different channel for file transfer (e.g., HTTP for files while using DNS for C2)
- Support caching and rate limiting on file transfers
- Prevent exploding DNS or other constrained channels with large file data
