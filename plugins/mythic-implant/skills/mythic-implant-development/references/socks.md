# SOCKS

This page describes how to implement SOCKS5 proxy support in a Mythic agent, including the message protocol, server-side RPC calls, and agent-side connection handling.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/socks

## Overview

SOCKS provides a way to tunnel TCP connections through the Mythic server, over the C2 channel, and out through the agent on the target network. This allows operators to proxy network tools (via proxychains, etc.) through Mythic and have them exit on the target.

Mythic implements SOCKS5 but does **not** leverage SOCKS5 authentication. If you open a SOCKS port on the Mythic server, you must lock it down with firewall rules.

### Traffic Flow

```
Operator tool (proxychains)
    -> Mythic server (SOCKS5 port)
    -> C2 channel (get_tasking/post_response messages)
    -> Agent on target
    -> TCP connection to destination IP:Port
```

## Server-Side: Starting and Stopping SOCKS

SOCKS is started and stopped via RPC calls from a command's `create_go_tasking` function. This is typically done in a dedicated `socks` command.

### Starting SOCKS (Python)

```python
from mythic_container.MythicGoRPC import *

async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
    response = PTTaskCreateTaskingMessageResponse(
        TaskID=taskData.Task.ID, Success=True,
    )
    # Start SOCKS on port 1080 on the Mythic server
    proxy_resp = await SendMythicRPCProxyStartCommand(MythicRPCProxyStartMessage(
        TaskID=taskData.Task.ID,
        LocalPort=1080,
        PortType="socks",  # CALLBACK_PORT_TYPE_SOCKS
    ))
    if not proxy_resp.Success:
        response.Success = False
        response.Error = proxy_resp.Error
    return response
```

### Stopping SOCKS (Python)

```python
proxy_resp = await SendMythicRPCProxyStopCommand(MythicRPCProxyStopMessage(
    TaskID=taskData.Task.ID,
    LocalPort=1080,
    PortType="socks",
))
```

### RPC Fields

| Field | Description |
|-------|-------------|
| `TaskID` | The task that initiated this proxy |
| `LocalPort` | Port to open on the Mythic server. Operators point proxychains here. |
| `PortType` | `"socks"` for SOCKS5 proxy |
| `RemotePort` | Not used for SOCKS (only used for RPFWD) |
| `RemoteIP` | Not used for SOCKS (only used for RPFWD) |

## Message Format

SOCKS data is carried in a `socks` array at the top level of `get_tasking` and `post_response` messages. It sits alongside `action`, `delegates`, `responses`, etc. - it is NOT inside a task response.

### Individual SOCKS Message

```json
{
    "exit": false,
    "server_id": 1234567,
    "data": "base64 encoded bytes"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `exit` | boolean | `true` = connection closed on one end, close the other end (after sending any remaining `data`). `false` = normal data transfer. |
| `server_id` | uint32 | Unique connection identifier. Mythic generates this for each new inbound proxy connection. |
| `data` | string | Base64-encoded TCP data. Can be empty string `""` if `exit` is `true` with no remaining data. In Python translation containers, `data` can be `None` when `exit` is `true`. |

### In get_tasking Messages

Mythic -> Agent: SOCKS data arrives in the response to `get_tasking`:

```json
{
    "action": "get_tasking",
    "tasks": [...],
    "socks": [
        {"exit": false, "server_id": 2, "data": "base64 string"},
        {"exit": true, "server_id": 1, "data": ""}
    ],
    "delegates": [...]
}
```

Agent -> Mythic: Agent sends SOCKS data in its `get_tasking` request:

```json
{
    "action": "get_tasking",
    "tasking_size": -1,
    "socks": [
        {"exit": false, "server_id": 2, "data": "base64 response data"},
        {"exit": false, "server_id": 3, "data": "base64 response data"}
    ]
}
```

### In post_response Messages

Same structure - the `socks` array can appear in both directions:

```json
{
    "action": "post_response",
    "responses": [...],
    "socks": [
        {"exit": false, "server_id": 2, "data": "base64 string"}
    ]
}
```

**Key point**: Any message to or from Mythic (`get_tasking` or `post_response`) can carry `socks` data. The agent must always check for and process a `socks` array in every response from Mythic, and should include any pending SOCKS data in every message it sends.

## Agent-Side Implementation

### Connection Lifecycle

1. **New connection**: Agent receives a `socks` message with an unknown `server_id`. This is a new proxy connection from an operator's tool.

2. **SOCKS5 request parsing**: The first message for a new `server_id` always contains a [SOCKS5 connect request](https://datatracker.ietf.org/doc/html/rfc1928#section-4). The `data` field (base64-decoded) contains the encoded destination IP and port. Mythic has already handled the SOCKS5 authentication/negotiation phase - the agent only sees the connect request.

3. **Connect to destination**: The agent parses the destination address from the SOCKS5 request and opens a TCP connection to it.

4. **SOCKS5 response**: The agent must send back a SOCKS5 connect response (per RFC 1928) indicating success or failure. This response goes back to Mythic in the `socks` array of the next outgoing message with the same `server_id`.

5. **Data forwarding**: Once connected, the agent forwards data bidirectionally:
   - Mythic -> Agent `socks` data: base64-decode and write to the TCP connection
   - TCP connection data: read, base64-encode, and send to Mythic in the `socks` array

6. **Connection close**: When either side closes:
   - If the target TCP connection closes: agent sends `{"exit": true, "server_id": X, "data": ""}` to Mythic
   - If Mythic sends `{"exit": true, ...}`: agent closes the corresponding TCP connection and cleans up resources

### SOCKS5 Connect Request Format (RFC 1928 Section 4)

The first `data` payload for a new `server_id` is a SOCKS5 request:

```
+----+-----+-------+------+----------+----------+
|VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
+----+-----+-------+------+----------+----------+
| 1  |  1  | X'00' |  1   | Variable |    2     |
+----+-----+-------+------+----------+----------+
```

- VER: `0x05` (SOCKS5)
- CMD: `0x01` (CONNECT)
- ATYP: `0x01` (IPv4), `0x03` (domain), `0x04` (IPv6)
- DST.ADDR: 4 bytes (IPv4), 1-byte length + string (domain), 16 bytes (IPv6)
- DST.PORT: 2 bytes, big-endian

### SOCKS5 Connect Response Format

The agent must reply with:

```
+----+-----+-------+------+----------+----------+
|VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
+----+-----+-------+------+----------+----------+
| 1  |  1  | X'00' |  1   | Variable |    2     |
+----+-----+-------+------+----------+----------+
```

- VER: `0x05`
- REP: `0x00` (success), `0x01` (general failure), `0x05` (connection refused)
- BND.ADDR/BND.PORT: the bound address (often zeroed out: `0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00`)

### Implementation Considerations

- **Concurrency**: Each `server_id` represents an independent TCP connection. The agent must handle many concurrent connections without exhausting system resources or causing deadlocks.
- **Buffering**: The agent should buffer data from open TCP connections and batch it into the `socks` array of outgoing messages, rather than sending one message per connection per read.
- **Cleanup**: When `exit` is received, close the TCP connection and free resources for that `server_id`. Do not leak goroutines/threads.
- **Error handling**: If the agent cannot connect to the destination, send back a SOCKS5 failure response and an `exit: true` message.

### Reference Implementation

The Poseidon agent (Go) has a working SOCKS implementation:
https://github.com/MythicAgents/poseidon/blob/master/Payload_Type/poseidon/poseidon/agent_code/socks/socks.go
