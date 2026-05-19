# Agent Message Format

This page describes the base wire format for all Mythic agent messages.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/agent-message-format

## Base Format

All agent messages follow this structure:

```
Base64(
    UUID + EncBlob(
        JSON({
            "action": "",      // required - what the message is
            "...": ...,        // required - action-specific data

            // optional - P2P mesh forwarding
            "delegates": [
                {"message": agentMessage, "c2_profile": "ProfileName", "uuid": "uuid here"},
                ...
            ]
        })
    )
)
```

## Components

### UUID (36 characters or 16 bytes)

The UUID prepended to the encrypted blob varies by agent phase:

| Phase | UUID Used | Purpose |
|-------|-----------|---------|
| Initial checkin | payloadUUID | Mythic looks up the payload, finds the C2 profile's AESPSK parameter for decryption |
| Staging (EKE) | tempUUID | Mythic looks up staging info (RSA state, DH state, etc.) |
| Established callback | callbackUUID | Mythic looks up the callback's encryption key |

Standard format: `b50a5fe8-099d-4611-a2ac-96d93e6ec77b` (36 chars)

Binary alternative: 16-byte big-endian UUID4 representation. If Mythic receives this format, it responds with the same format. Currently only supported for egress messages, not P2P.

### EncBlob (Encrypted Blob)

The encryption depends on the phase:
- **Plaintext**: No encryption (testing only, C2 profile crypto parameter set to `none`)
- **AES256**: Static pre-shared key or negotiated session key
- **RSA**: During key exchange only
- **Custom**: Via translation container

### JSON Body

The `action` field determines the message type:

| Action | Direction | Description |
|--------|-----------|-------------|
| `staging_rsa` | Agent -> Mythic | RSA key exchange initiation |
| `checkin` | Agent -> Mythic | Register as a callback |
| `get_tasking` | Agent -> Mythic | Request pending tasks |
| `post_response` | Agent -> Mythic | Submit task results |
| `staging_translation` | Internal | Custom EKE via translation container |

### Delegates (P2P Forwarding)

The `delegates` array carries messages from linked P2P agents. Each entry is a self-contained agent message:

```json
{
    "message": "<complete base64-encoded agentMessage>",
    "c2_profile": "tcp",
    "uuid": "uuid of the delegate agent"
}
```

If your agent is not doing P2P forwarding, omit this field entirely.

### Byte Concatenation

The `+` operator in the format means raw byte concatenation. After the UUID bytes, immediately append the encrypted blob bytes. No separator, no length prefix.

## Concrete Examples (Plaintext, Base64-Decoded)

### Checkin

```
a21bab2e-462e-49ab-9800-fbedaf53ad15
{
    "action": "checkin",
    "uuid": "a21bab2e-462e-49ab-9800-fbedaf53ad15",
    "user": "bob",
    "domain": "domain.com",
    "pid": 123
}
```

### Get Tasking

```
a21bab2e-462e-49ab-9800-fbedaf53ad15
{
    "action": "get_tasking",
    "tasking_size": -1
}
```

### Post Response

```
a21bab2e-462e-49ab-9800-fbedaf53ad15
{
    "action": "post_response",
    "responses": [
        {
            "task_id": "c34bab2e-462e-49ab-9800-fbedaf53ad15",
            "completed": true,
            "user_output": "hello world"
        }
    ]
}
```

### Get Tasking with P2P Delegates

```
a21bab2e-462e-49ab-9800-fbedaf53ad15
{
    "action": "get_tasking",
    "tasking_size": -1,
    "delegates": [
        {"message": "<agentMessage>", "c2_profile": "tcp", "uuid": "uuid here"},
        {"message": "<agentMessage>", "c2_profile": "smb", "uuid": "uuid here"}
    ]
}
```

## Transport

All messages go to the `/agent_message` endpoint via the C2 profile container. Messages can be delivered via:

- **POST request**: message content in body
- **GET request**: message content in:
  - First header value
  - First cookie value
  - First query parameter (must use URL-safe Base64: `+` -> `-`, `/` -> `_`)
  - Request body

## Custom Agent Message Format

If you want a completely custom wire format (binary protocol, different field names, etc.), only two things are required:

1. Base64 encode the message
2. First bytes must be the UUID (payload, staging, or callback)

Mythic uses the UUID to look up the payload type and check for a translation container. If one exists, the raw message is forwarded to it for conversion to standard Mythic JSON.
