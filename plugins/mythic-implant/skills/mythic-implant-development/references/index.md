# Mythic Implant Development - Reference Index

This index lists all reference documentation available for Mythic agent development. Load only the pages you need to conserve context window space.

## Phase 1: Project Setup

| Page | Description |
|------|-------------|
| [Project Layout](./project-layout.md) | Container structure, Dockerfile templates, folder layout, main.py/main.go, External Agent repo format |
| [Container Syncing](./container-syncing.md) | How containers register with Mythic, sync triggers, cascading sync behavior |

## Phase 2: Agent Communication Protocol

| Page | Description |
|------|-------------|
| [Agent Message Format](./agent-message-format.md) | Base wire format: `Base64(UUID + EncBlob(JSON))`, UUID types, encryption blob structure, delegate messages |
| [Initial Checkin](./initial-checkin.md) | Plaintext checkin, static AES256, RSA encrypted key exchange, custom EKE, all crypto details |
| [Get Tasking](./get-tasking.md) | Request/response format for fetching tasks, tasking_size, delegate forwarding |
| [Post Response](./post-response.md) | Submitting task output, completion status, error handling, process_response hook |
| [File Downloads](./file-downloads.md) | Agent -> Mythic chunked file transfer protocol, registration, chunk numbering |
| [File Uploads](./file-uploads.md) | Mythic -> Agent chunked file pull protocol, File parameter UUIDs, RPC file access |

## Phase 3: Commands and Features

| Page | Description |
|------|-------------|
| [Commands](./commands.md) | CommandBase class, TaskArguments, CommandParameters, parameter types, parameter groups |
| [Create Tasking](./create-tasking.md) | create_go_tasking function, available context, RPC calls, DisplayParams, completion functions |
| [OPSEC Checking](./opsec-checking.md) | opsec_pre/opsec_post functions, blocking, bypass roles, execution order |

## Phase 4: Agent Definition and Build

| Page | Description |
|------|-------------|
| [Payload Type Definition](./payload-type-definition.md) | PayloadType class (Python + Go), BuildParameter types, build function, BuildResponse, build steps, on_new_callback |

## Phase 5: Advanced Features

| Page | Description |
|------|-------------|
| [SOCKS](./socks.md) | SOCKS5 proxy through agent, message format, server_id tracking, RPC start/stop |
| [Reverse Port Forward](./rpfwd.md) | Reverse port forward through agent, agent-initiated connections, RPC start/stop |
| [Translation Containers](./translation-containers.md) | Custom message formats, custom encryption, staging_translation flow, gRPC transport |
| [C2 Profile Definition](./c2-profile-definition.md) | C2Profile class, parameters, server_binary_path, P2P vs egress profiles |
| [P2P Connections](./p2p-connections.md) | Edge reporting, delegate message format, automatic connection announcements |
