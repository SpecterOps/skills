# C2 Profile Definition

This page describes how to define a C2 profile for Mythic, including parameters and server-side code.

Source: https://docs.mythic-c2.net/customizing/c2-related-development/mythic-definition/2.1.1-c2-class-definition

## What Are C2 Profiles

C2 profiles are Docker containers that act as forwarding mechanisms between your agent's communication protocol and Mythic's internal HTTP POST format. Their role is to get data off the wire and forward it to Mythic.

Key properties:
- C2 protocols are decoupled from agents - multiple agent types can share a C2 profile
- Written in any language (Go, Python, C#, etc.)
- Live in their own Docker containers
- Payload types register which C2 profiles they support

## C2Profile Class (Python)

```python
from mythic_container.C2ProfileBase import *
import pathlib

class MyC2(C2Profile):
    name = "myc2"
    description = "My custom C2 profile"
    author = "@you"
    is_p2p = False
    semver = "0.0.1"
    agent_icon_path = pathlib.Path(".") / "myc2.svg"
    server_binary_path = pathlib.Path(".") / "myc2_executable"
    server_folder_path = pathlib.Path(".")
    parameters = [
        C2ProfileParameter(
            name="callback_host",
            description="Callback host in URL format",
            default_value="https://mythic.example.com",
            verifier_regex="^(http|https)://[a-zA-Z0-9]+",
            required=True,
        ),
        C2ProfileParameter(
            name="callback_port",
            description="Callback port",
            default_value="443",
            verifier_regex="^[0-9]+$",
            required=True,
        ),
        C2ProfileParameter(
            name="callback_interval",
            description="Seconds between callbacks",
            default_value="10",
            required=True,
        ),
        C2ProfileParameter(
            name="callback_jitter",
            description="Jitter percentage (0-100)",
            default_value="23",
            required=True,
        ),
        C2ProfileParameter(
            name="AESPSK",
            description="Encryption key",
            default_value="aes256_hmac",
            parameter_type=C2ProfileParameterType.ChooseOne,
            choices=["aes256_hmac", "none"],
            required=False,
            crypto_type=True,
        ),
        C2ProfileParameter(
            name="headers",
            description="HTTP headers",
            parameter_type=C2ProfileParameterType.Dictionary,
            dictionary_choices=[
                C2ProfileDictionaryChoice(
                    name="User-Agent",
                    default_value="Mozilla/5.0",
                    default_show=True,
                ),
            ],
        ),
    ]
```

## C2 Definition (GoLang)

```go
var myC2Definition = c2structs.C2Profile{
    Name:             "myc2",
    Author:           "@you",
    Description:      "My custom C2 profile",
    IsP2p:            false,
    SemVer:           "0.0.1",
    ServerBinaryPath: filepath.Join(".", "myc2_executable"),
    ServerFolderPath: filepath.Join("."),
}

func Initialize() {
    c2structs.AllC2Data.Get("myc2").AddC2Definition(myC2Definition)
    // Add parameters, server routes, etc.
}
```

## Key Fields

| Field | Description |
|-------|-------------|
| `name` | Profile name (used by payload types to declare support) |
| `is_p2p` | `True` for P2P profiles (no server-side code to run), `False` for egress profiles |
| `server_binary_path` | Path to executable that handles C2 traffic. For scripted languages, add `#! python` shebang. |
| `server_folder_path` | Folder shown when browsing container files in UI. Contains `config.json`. |

## C2 Profile Parameters

Parameters define the configurable options operators see when building payloads:

| Attribute | Description |
|-----------|-------------|
| `name` | Unique key per profile. Used in `get_parameters_dict()` during build. |
| `description` | Shown to operator |
| `default_value` | Default if operator doesn't change it |
| `verifier_regex` | UI validation regex |
| `required` | Must have a value |
| `randomized` | Randomize per payload build |
| `format_string` | Regex format for randomization (e.g., `[a-z0-9]{8}-[a-z0-9]{4}-...` for UUID) |
| `crypto_type` | If `True`, Mythic generates enc_key/dec_key and provides them during build |
| `parameter_type` | String, ChooseOne, ChooseMultiple, Dictionary, Array, Boolean, Date, File |

### crypto_type Parameter

When `crypto_type=True`, Mythic:
1. Generates encryption keys (AES256 or via translation container)
2. Stores them in the database
3. Provides them during build via `c2info.get_parameters_dict()`
4. Uses them to decrypt/encrypt agent messages

The value returned is a dict: `{"value": "user selection", "enc_key": "base64 or None", "dec_key": "base64 or None"}`

### Dictionary Parameters

For parameters like HTTP headers:

```python
C2ProfileParameter(
    name="headers",
    parameter_type=C2ProfileParameterType.Dictionary,
    dictionary_choices=[
        C2ProfileDictionaryChoice(
            name="User-Agent",
            default_value="Mozilla/5.0",
            default_show=True,
        ),
        C2ProfileDictionaryChoice(
            name="Host",
            default_value="",
            default_show=False,
        ),
    ],
)
```

Agent receives: `{"User-Agent": "value", "Host": "value"}`

## Egress vs P2P Profiles

### Egress Profile
- `is_p2p = False`
- Has server-side code (opens ports, listens for connections)
- Forwards agent traffic to Mythic's `/agent_message` endpoint
- Example: HTTP, DNS, WebSocket

### P2P Profile
- `is_p2p = True`
- No server-side code (communication logic is in the agents)
- Parameters still define how agents connect to each other
- Example: TCP, SMB named pipes

## Server-Side Code

The `server_binary_path` executable is what actually handles traffic:

- Opens ports, connects to third-party services, etc.
- Receives agent messages
- Forwards to Mythic at `https://mythic_server:mythic_port/agent_message`
- Returns Mythic's response to the agent

The server code can also implement:
- OPSEC checks for C2 configurations
- Configuration validation
- Sample message generation
- Redirect rule generation
- File hosting
- IOC reporting

## How Agents Declare C2 Support

In the payload type definition:

```python
# Python
c2_profiles = ["http", "websocket", "myc2"]

# Go
SupportedC2Profiles: []string{"http", "websocket", "myc2"},
```

When building a payload, the operator selects which C2 profiles to include. The build function receives the selected profiles and their parameter values.
