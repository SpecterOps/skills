# Reverse Port Forward

This page describes how to implement reverse port forwarding in a Mythic agent, including the message protocol, server-side RPC calls, and agent-side connection handling.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/rpfwd

## Overview

Reverse port forwarding allows an agent to open a listening port on the target host. When something connects to that port, the traffic is tunneled back through the C2 channel to Mythic, which then connects out to a specified remote IP:Port. This exposes an internal service to the operator's network.

### Traffic Flow

```
Service on target network
    -> Agent listening port (on target)
    -> C2 channel (get_tasking/post_response messages)
    -> Mythic server
    -> TCP connection to RemoteIP:RemotePort
```

This is the reverse of SOCKS: with SOCKS the operator initiates connections that exit at the agent; with RPFWD the target network initiates connections that exit at Mythic.

## Server-Side: Starting and Stopping RPFWD

RPFWD is started and stopped via the same RPC calls as SOCKS, but with different parameters.

### Starting RPFWD (Python)

```python
from mythic_container.MythicGoRPC import *

async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
    response = PTTaskCreateTaskingMessageResponse(
        TaskID=taskData.Task.ID, Success=True,
    )
    # Agent opens port 8080 on target; Mythic forwards to 10.0.0.5:80
    proxy_resp = await SendMythicRPCProxyStartCommand(MythicRPCProxyStartMessage(
        TaskID=taskData.Task.ID,
        LocalPort=8080,       # Port agent opens on target
        RemoteIP="10.0.0.5",  # Where Mythic connects when traffic arrives
        RemotePort=80,         # Port Mythic connects to
        PortType="rpfwd",     # CALLBACK_PORT_TYPE_RPORTFWD
    ))
    if not proxy_resp.Success:
        response.Success = False
        response.Error = proxy_resp.Error
    return response
```

### Stopping RPFWD (Python)

```python
proxy_resp = await SendMythicRPCProxyStopCommand(MythicRPCProxyStopMessage(
    TaskID=taskData.Task.ID,
    LocalPort=8080,
    PortType="rpfwd",
))
```

### RPC Fields

| Field | Description |
|-------|-------------|
| `TaskID` | The task that initiated this proxy |
| `LocalPort` | Port the agent opens on the target host |
| `RemoteIP` | IP address Mythic connects to when traffic arrives from the agent |
| `RemotePort` | Port Mythic connects to at RemoteIP |
| `PortType` | `"rpfwd"` for reverse port forward |

## Message Format

RPFWD data is carried in an `rpfwd` array at the top level of `get_tasking` and `post_response` messages, alongside `action`, `socks`, `delegates`, etc.

### Individual RPFWD Message

```json
{
    "exit": false,
    "server_id": 1234567,
    "data": "base64 encoded bytes",
    "port": 8080
}
```

| Field | Type | Description |
|-------|------|-------------|
| `exit` | boolean | `true` = connection closed, close the other end. `false` = normal data. |
| `server_id` | uint32 | Unique connection identifier. **The agent generates this** (unlike SOCKS where Mythic generates it). |
| `data` | string | Base64-encoded TCP data. Can be empty/`None` when `exit` is `true`. |
| `port` | uint32 | Optional but recommended. The local port on the agent where the connection was received. **Required if the agent supports multiple concurrent rpfwd listeners**, so Mythic can route traffic to the correct RemoteIP:RemotePort. |

### Key Difference from SOCKS

| | SOCKS | RPFWD |
|--|-------|-------|
| Who generates `server_id` | Mythic | Agent |
| Who initiates connections | Operator's tools | Target network services |
| Extra field | None | `port` (optional) |
| `RemoteIP`/`RemotePort` in RPC | Not used | Required (where Mythic connects) |

### In get_tasking Messages

Agent -> Mythic: Agent sends new connection data and ongoing traffic:

```json
{
    "action": "get_tasking",
    "tasking_size": -1,
    "rpfwd": [
        {"exit": false, "server_id": 2, "data": "base64 string", "port": 8080},
        {"exit": true, "server_id": 1, "data": "", "port": 8080}
    ]
}
```

Mythic -> Agent: Mythic sends response data back:

```json
{
    "action": "get_tasking",
    "tasks": [...],
    "rpfwd": [
        {"exit": false, "server_id": 2, "data": "base64 response data", "port": 8080}
    ]
}
```

### In post_response Messages

Same structure - the `rpfwd` array can appear in both directions:

```json
{
    "action": "post_response",
    "responses": [...],
    "rpfwd": [
        {"exit": false, "server_id": 2, "data": "base64 string", "port": 8080}
    ]
}
```

**Key point**: Like SOCKS, the agent must check for `rpfwd` data in every response from Mythic and include pending RPFWD data in every outgoing message.

## Agent-Side Implementation

### Connection Lifecycle

1. **Open listener**: When the rpfwd command is tasked, the agent opens the specified `LocalPort` on the target host.

2. **Accept connection**: A service on the target network connects to the agent's listening port. The agent accepts the connection and generates a random `uint32` value as the `server_id`.

3. **Forward initial data**: The agent reads data from the new connection and sends it to Mythic in the `rpfwd` array with the new `server_id` and the `port` the connection arrived on.

4. **Mythic connects out**: Mythic receives the data, sees an unknown `server_id`, creates a new TCP connection to `RemoteIP:RemotePort`, and forwards the data. Any response data from the remote end is sent back to the agent in the `rpfwd` array.

5. **Data forwarding**: The agent forwards data bidirectionally:
   - Mythic -> Agent `rpfwd` data: base64-decode and write to the local TCP connection
   - Local TCP connection data: read, base64-encode, send to Mythic in the `rpfwd` array

6. **Connection close**: When either side closes:
   - If the local TCP connection closes: agent sends `{"exit": true, "server_id": X, "data": "", "port": Y}`
   - If Mythic sends `{"exit": true, ...}`: agent closes the corresponding TCP connection

### Implementation Considerations

- **server_id generation**: The agent must generate unique random uint32 values for each new connection. Collisions would cause routing issues.
- **Multiple listeners**: If the agent supports multiple rpfwd ports simultaneously, always include the `port` field so Mythic routes to the correct RemoteIP:RemotePort.
- **Concurrency**: Same concerns as SOCKS - handle many concurrent connections without resource exhaustion or deadlocks.
- **Cleanup**: When the rpfwd command is stopped, close all accepted connections and the listening socket. Send `exit: true` for all active `server_id` values.
- **Error handling**: If the agent cannot open the listening port, report an error back via the task response.

### Reference Implementation

The Poseidon agent (Go) has a working RPFWD implementation:
https://github.com/MythicAgents/poseidon/blob/master/Payload_Type/poseidon/poseidon/agent_code/rpfwd/rpfwd.go
