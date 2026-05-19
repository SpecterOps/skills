# File Downloads (Agent -> Mythic)

This page describes the chunked file transfer protocol for downloading files from a target through the agent to the Mythic server.

Source: https://docs.mythic-c2.net/customizing/hooking-features/download

## Overview

File downloads are chunked transfers that require multiple round-trips:

1. Agent locates the file and determines its size
2. Agent registers the file with Mythic (gets a file UUID)
3. Agent sends chunks one at a time
4. Mythic acknowledges each chunk

This allows Mythic to track progress and handle large files through constrained C2 channels.

## Step 1: Register the File

Agent sends as part of a `post_response`:

```json
{
    "action": "post_response",
    "responses": [
        {
            "task_id": "UUID of the download task",
            "download": {
                "total_chunks": 4,
                "full_path": "/test/test2/file.txt",
                "host": "hostname",
                "filename": "display name",
                "is_screenshot": false,
                "chunk_size": 512000
            }
        }
    ]
}
```

### Registration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `total_chunks` | Yes | Number of chunks. Use `-1` if unknown (update later). |
| `full_path` | No | Full filesystem path. Allows Mythic to track files across callbacks. |
| `host` | No | Hostname the file is on. Defaults to callback's hostname if empty. |
| `filename` | No | Display name if `full_path` doesn't make sense (e.g., "screenshot 1", "lsass dump"). |
| `is_screenshot` | No | `true` for screenshots (shown on screenshot page), `false`/omitted for files. Default: `false`. |
| `chunk_size` | No | Bytes per chunk. Can be provided here or with first data chunk. Required if sending chunks out of order. |

### Registration Response

Mythic returns a `file_id`:

```json
{
    "action": "post_response",
    "responses": [
        {
            "status": "success",
            "file_id": "UUID-for-this-file",
            "task_id": "task uuid"
        }
    ]
}
```

## Step 2: Send Chunks

For each chunk, send:

```json
{
    "action": "post_response",
    "responses": [
        {
            "task_id": "task uuid",
            "download": {
                "chunk_num": 1,
                "file_id": "UUID from registration",
                "chunk_data": "base64 encoded chunk",
                "chunk_size": 512000
            }
        }
    ]
}
```

### Chunk Fields

| Field | Required | Description |
|-------|----------|-------------|
| `chunk_num` | Yes | **1-based**. First chunk is `1`, not `0`. |
| `file_id` | Yes | The UUID returned from registration. |
| `chunk_data` | Yes | Base64-encoded file data for this chunk. |
| `chunk_size` | Conditional | Required if not sent during registration and planning to send chunks out of order. This is the standard chunk size (not the size of the current chunk). |

**Why 1-based chunk_num?** Legacy from Mythic 1.0 Python implementation where `0` was ambiguous with unset fields.

### Chunk Response

```json
{
    "action": "post_response",
    "responses": [
        {
            "status": "success",
            "task_id": "task uuid"
        }
    ]
}
```

## Out-of-Order Chunks

Mythic supports receiving chunks out of order. Requirements:
- `chunk_size` must be provided (either at registration or with the first chunk)
- Mythic uses `chunk_size` to seek to the correct position in the file on disk
- The last chunk may be smaller than `chunk_size`

## Unknown Total Chunks

If the agent cannot determine file size ahead of time:
1. Register with `total_chunks: -1`
2. Send chunks normally
3. Include `total_chunks` with the correct value in any subsequent chunk message to update it

## Additional Keys

Any extra keys in the agent's messages will be echoed back by Mythic. Agents can use this to include their own file transfer identifiers for tracking multiple concurrent transfers.

## Strongly-Typed Languages

If your agent language requires all fields in every message, set `total_chunks` to `null` (not `0` or any number) in chunk messages. Otherwise Mythic will interpret it as a new file registration.
