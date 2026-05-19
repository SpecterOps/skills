# Mythic Implant Development

A Claude Code skill for building Mythic C2 framework agents from scratch.

## Purpose

Guides the step-by-step development of a new Mythic agent (implant/payload), from project layout through agent-to-Mythic communication, command implementation, and server-side Python/Go definitions.

The skill splits the Mythic documentation into context-efficient reference pages that are loaded on-demand, keeping the LLM context window focused on what's needed.

## Prerequisites

- A running Mythic instance (v3.3+)
- Docker environment for building agent containers
- Familiarity with at least one systems programming language (Go, C, C#, Rust, etc.)

## What This Skill Covers

1. **Project Layout** - Container structure, Dockerfiles, External Agent template format
2. **Agent Communication** - Message format, checkin, key exchange, get/post tasking, file transfer
3. **Commands** - CommandBase definitions, TaskArguments, parameter types, parameter groups
4. **Payload Type Definition** - Build parameters, build function, BuildResponse
5. **OPSEC** - No hardcoded strings, no debug output, opsec_pre/opsec_post checks
6. **Advanced Features** - Translation containers, P2P mesh, custom C2 profiles

## Usage

The skill activates when you ask to build a Mythic agent. It will first prompt you for:

- **C2 channel** (HTTP, DNS, SMB, TCP, WebSocket, custom)
- **Target platforms** (Windows, macOS, Linux)
- **Agent language** (Go, C, C#, Rust, Python, etc.)
- **Commands** to implement
- **Encryption model** (plaintext, AES256, RSA EKE, custom)
- **Container language** (Python or GoLang for server-side definitions)

## Reference Pages

| Page | Description |
|------|-------------|
| `project-layout.md` | Container structure, Dockerfile, folder layout |
| `payload-type-definition.md` | PayloadType class, build params, build function |
| `agent-message-format.md` | Base wire format, UUID handling, encryption |
| `initial-checkin.md` | All checkin methods and key exchange protocols |
| `get-tasking.md` | Task request/response format |
| `post-response.md` | Submitting task results |
| `file-downloads.md` | Agent -> Mythic chunked file transfer |
| `file-uploads.md` | Mythic -> Agent chunked file pull |
| `commands.md` | Command and parameter definitions |
| `create-tasking.md` | Server-side task preprocessing and RPC |
| `opsec-checking.md` | Pre/post OPSEC gates |
| `socks.md` | SOCKS5 proxy protocol and agent implementation |
| `rpfwd.md` | Reverse port forward protocol and agent implementation |
| `translation-containers.md` | Custom message formats and crypto |
| `c2-profile-definition.md` | C2 profile class and parameters |
| `p2p-connections.md` | Peer-to-peer agent mesh |
| `container-syncing.md` | Container registration lifecycle |

## Documentation Source

All reference material is derived from the official Mythic documentation at https://docs.mythic-c2.net/
