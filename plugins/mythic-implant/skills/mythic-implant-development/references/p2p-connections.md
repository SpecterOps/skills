# P2P Connections

This page describes how agents report peer-to-peer connections and forward delegate messages.

Source: https://docs.mythic-c2.net/customizing/hooking-features/linking-agents/action-p2p_info

## Overview

P2P connections allow agents to communicate through each other in a mesh network. The egress agent (with external connectivity) forwards messages for linked P2P agents.

Mythic uses edge reports to construct a connectivity graph for routing and display.

## Reporting Edges

Agents report new or removed connections:

```json
{
    "user_output": "linked to agent on \\\\TARGET\\pipe\\pipename",
    "task_id": "uuid of the link task",
    "edges": [
        {
            "source": "uuid of source callback",
            "destination": "uuid of destination callback",
            "metadata": "{ optional metadata json string }",
            "action": "add",
            "c2_profile": "smb"
        }
    ]
}
```

### Edge Fields

| Field | Required | Description |
|-------|----------|-------------|
| `source` | Yes | One end of the connection (usually the reporting agent) |
| `destination` | Yes | The other end of the connection |
| `metadata` | No | Additional info (e.g., pipe name, port number) |
| `action` | Yes | `"add"` for new connection, `"remove"` for disconnection |
| `c2_profile` | Yes | Name of the C2 profile used for this P2P link |

### Edge Reporting Outside of Tasks

The `edges` array can be sent outside of a `responses` array - as a top-level field in any message. This is useful when a link drops unexpectedly (not due to a task) and the agent needs to inform Mythic.

### Response from Mythic

```json
{
    "status": "success",
    "error": "",
    "task_id": "task uuid"
}
```

## Delegate Messages

Delegate messages are how P2P agent traffic flows through the egress agent.

### In get_tasking / post_response

```json
{
    "action": "get_tasking",
    "tasking_size": -1,
    "delegates": [
        {
            "message": "<complete base64 agentMessage from linked agent>",
            "c2_profile": "tcp",
            "uuid": "uuid of the linked agent"
        }
    ]
}
```

Each delegate message is a self-contained agent message (UUID + encrypted JSON, base64 encoded). The `c2_profile` tells Mythic how to decode/translate it.

Mythic processes each delegate message independently and returns responses in the same `delegates` array format.

### Delegate responses from Mythic

```json
{
    "action": "get_tasking",
    "tasks": [...],
    "delegates": [
        {
            "message": "<response agentMessage for linked agent>",
            "c2_profile": "tcp",
            "uuid": "uuid of the linked agent"
        }
    ]
}
```

The egress agent must forward these response messages to the appropriate linked agent.

## Automatic Connection Detection

When an egress agent sends a message with a `delegates` component, Mythic automatically creates a route between the two agents. You should still explicitly report edges for proper tracking, but Mythic handles the common case.

## Linked Agent Checkin

When a P2P agent first links, it should send a checkin message (or re-send if already checked in). This forces Mythic to become aware of the connection between the two callbacks.

## get_delegate_tasks

In `get_tasking`, the `get_delegate_tasks` field (default: `true`) controls whether the egress agent also picks up tasks for reachable P2P agents:

- `true`: Fetch tasks for linked agents too
- `false`: Only fetch tasks for this agent (useful when linked agents do their own periodic `get_tasking`)
