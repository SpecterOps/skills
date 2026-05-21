---
name: mythic-implant-development
description: Provides guidance and documentation for building Mythic C2 framework agents/implants from scratch
license: MIT
metadata:
  author: xpn
  version: "0.1.0"
  category: security
icon: ./assets/icon.png
---

# Mythic Implant Development Skill

## When to Use

Use this skill when developing a new agent (implant/payload) for the Mythic C2 framework. This includes:

- "Build a new Mythic agent in Go/Rust/C/C#/Python"
- "Create a Mythic implant that supports HTTP C2"
- "Port this agent to work with Mythic"
- "Add a new command to my Mythic payload type"

## When NOT to Use

Do not use this skill for:

- General Mythic server administration or installation
- Developing standalone tools unrelated to Mythic
- Working with other C2 frameworks (Cobalt Strike, Sliver, etc.)

## Initial Requirements Gathering

**CRITICAL**: Before writing any code, you MUST ask the user the following clarification questions. Do not assume defaults. Each answer significantly impacts the architecture.

1. **C2 Channel**: What communication channel should the agent use?
   - Egress: HTTP, HTTPS, DNS, WebSocket, custom
   - P2P: TCP, SMB named pipes, custom
   - Multiple channels in a single agent?

2. **Target Platforms**: What operating systems will the agent support?
   - Windows, macOS, Linux, or a combination
   - Architecture: x64, ARM64, both

3. **Agent Language**: What language or framework should the agent be written in?
   - Go, C, C++, C#/.NET, Rust, Python, Nim, etc.
   - This is the language of the agent itself (runs on target)
   - The Mythic container definitions (server-side) can be in Python or GoLang independently of the agent language

4. **Commands**: What commands should the agent support initially?
   - Common starting set: shell execution, file upload/download, process listing, directory listing, change directory, exit
   - Any specialized capabilities needed?

5. **Encryption**: What key exchange / encryption model?
   - Plaintext (testing only)
   - Static AES256 pre-shared key
   - RSA encrypted key exchange (recommended for production)
   - Custom EKE via translation container

6. **Mythic Container Language**: Should the server-side definitions (commands, build logic) be written in Python or GoLang?

## OPSEC Requirements

**OPSEC is the highest priority throughout all development.** Every piece of code produced must adhere to the following:

### Mandatory OPSEC Rules

1. **No hardcoded attributable strings** - Never embed tool names, author names, framework identifiers, or any string that would allow attribution to the agent, its developer, or the C2 framework. This includes:
   - User-Agent strings that identify the framework
   - Mutex names containing tool/framework names
   - Registry key names or values containing identifiable strings
   - Named pipe names with identifiable prefixes
   - Window class names or window titles

2. **No embedded debug messages** - Never include debug print statements, logging calls, or verbose error messages in production agent code. Debug output must be:
   - Gated behind a compile-time flag that is OFF by default
   - Completely stripped from release builds
   - Never contain function names, file paths, or developer-identifiable information

3. **String handling** - All strings that could be signatured should be:
   - Constructed at runtime where possible
   - Obfuscated or encrypted at rest in the binary
   - Never stored as plaintext string literals in the final binary

4. **Network indicators** - Minimize network-level signatures:
   - Randomize or make configurable: callback intervals, jitter, URI paths, headers
   - Do not use default or well-known URI patterns
   - Support configurable HTTP headers and request formatting

5. **Build artifacts** - Ensure clean builds:
   - Strip debug symbols in release builds
   - Remove or obfuscate Go build paths (if using Go)
   - Avoid leaving compiler metadata that reveals the build environment

6. **Mythic OPSEC hooks** - Implement `opsec_pre` and `opsec_post` checks on commands that create detectable artifacts (process creation, file writes, network connections). See [OPSEC Checking](./references/opsec-checking.md).

### When Generating Code

- Always ask: "Would this string/pattern be signaturable?"
- Always ask: "Does this leave unnecessary artifacts?"
- If a user requests something that conflicts with OPSEC (e.g., hardcoded debug output), warn them explicitly and suggest the OPSEC-safe alternative.

## Development Workflow

Follow these steps in order. Each step references documentation pages that should be loaded for detailed specifications.

### Step 1: Project Layout

Create the Mythic-compatible project structure. This is critical - Mythic expects a specific folder layout for the container to sync properly.

**Read**: [Project Layout](./references/project-layout.md)

Key deliverables:
- `Dockerfile` using appropriate Mythic base image
- `main.py` or `main.go` entry point for the Mythic container
- Agent source code directory
- Proper folder naming (lowercase, no capitals - Docker limitation)

The project should follow the External Agent template format:
```
your-agent/
  Payload_Type/
    your_agent_name/
      Dockerfile
      main.py (or main.go + Makefile)
      your_agent_name/
        mythic/
          agent_functions/
            builder.py (or agentfunctions/*.go)
            command1.py
            command2.py
            ...
        agent_code/
          <your agent source code in whatever language>
```

### Step 2: Build Dependencies

Set up the build environment within the Docker container.

**CRITICAL**: The `build()` function runs INSIDE the container. Docker is NOT available inside the container. All compilers and tools your agent needs must be installed in the Dockerfile. You cannot use `docker build`, `docker run`, or any Docker-in-Docker commands from the build function.

- Select the appropriate Mythic base image for your container language:
  - `itsafeaturemythic/mythic_python_base:latest` - Python definitions
  - `itsafeaturemythic/mythic_go_base:latest` - Go definitions
  - `itsafeaturemythic/mythic_python_go:latest` - Python definitions + Go compiler
  - `itsafeaturemythic/mythic_go_macos:latest` - Go definitions + macOS SDK
  - `itsafeaturemythic/mythic_python_macos:latest` - Python definitions + macOS SDK
  - `itsafeaturemythic/mythic_go_dotnet:latest` - Go definitions + .NET SDK

- Install any additional build tools in the Dockerfile via `RUN` commands (Rust toolchain, cross-compilers, MinGW, etc.)
- For Go-based containers, create a `Makefile` with `build` and `run` targets
- The agent code is compiled inside this container when the `build()` function calls compilers/tools via `subprocess` (Python) or `os/exec` (Go)

### Step 3: Agent-to-Mythic Communication

This is the core of the agent. Implement the message protocol in the agent's language.

**Read these references in order**:
1. [Agent Message Format](./references/agent-message-format.md) - The base wire format: `Base64(UUID + EncBlob(JSON))`
2. [Initial Checkin](./references/initial-checkin.md) - How the agent registers with Mythic
3. [Get Tasking](./references/get-tasking.md) - How the agent requests tasks
4. [Post Response](./references/post-response.md) - How the agent returns task output
5. [File Downloads](./references/file-downloads.md) - Agent -> Mythic file transfer
6. [File Uploads](./references/file-uploads.md) - Mythic -> Agent file transfer

Implementation order within the agent:
1. **Message encoding/decoding** - Base64, JSON serialization, UUID handling
2. **Encryption layer** - AES256-CBC with PKCS7 padding, HMAC-SHA256 (if using encrypted comms). Format: `IV (16 bytes) + Ciphertext + HMAC`
3. **HTTP/transport layer** - The actual network communication matching the C2 profile
4. **Checkin** - First contact with Mythic, exchange payload UUID for callback UUID
5. **Key exchange** - If using RSA EKE: generate 4096-bit RSA keypair, send public key, receive AES session key
6. **Task loop** - `get_tasking` on interval, process commands, `post_response` with results
7. **File transfer** - Chunked upload/download protocol with file UUID tracking

### Step 4: Commands and Features

Add the commands the user requested. Each command has two parts:
- **Agent-side**: The code in the agent that executes the command
- **Mythic-side**: The Python/Go definition that tells Mythic about the command

**Read**: [Commands](./references/commands.md) and [Create Tasking](./references/create-tasking.md)

For each command:
1. Define `CommandBase` / command struct with metadata (name, description, MITRE ATT&CK mapping, help text)
2. Define `TaskArguments` / argument struct with parameters
3. Implement `create_go_tasking` for any server-side preprocessing
4. Implement the agent-side execution logic
5. Add `opsec_pre`/`opsec_post` checks where the command creates detectable artifacts

For additional features, consult:
- [SOCKS](./references/socks.md) - SOCKS5 proxy tunneling through the agent
- [Reverse Port Forward](./references/rpfwd.md) - Reverse port forwarding through the agent
- [Translation Containers](./references/translation-containers.md) - Custom message formats / crypto
- [P2P Connections](./references/p2p-connections.md) - Peer-to-peer mesh networking
- [OPSEC Checking](./references/opsec-checking.md) - Pre/post task OPSEC gates

### Step 5: Mythic-Side Python/Go Scripts

Create the server-side container code that defines the agent to Mythic.

**Read**: [Payload Type Definition](./references/payload-type-definition.md)

Key deliverables:
1. **Payload Type class** - Name, supported OS, C2 profiles, build parameters, file extension
   - **Python field names**: `name`, `supported_os`, `c2_profiles` (NOT `supported_c2_profiles`), `build_parameters`, `mythic_encrypts`
   - **Go struct fields**: `Name`, `SupportedOS`, `SupportedC2Profiles`, `BuildParameters`, `MythicEncryptsData`
2. **Build function** - Takes user-selected options and compiles/assembles the agent binary
   - Runs INSIDE the container - only tools installed in the Dockerfile are available
   - Read C2 profile parameters and stamp them into agent config
   - Call compilers via `subprocess` (Python) or `os/exec` (Go)
   - Handle command selection (if `supports_dynamic_loading`)
   - Return `BuildResponse` with the final payload bytes
3. **Command definitions** - One file per command with `CommandBase` and `TaskArguments`
4. **Build steps** - Define progress indicators for the build process

See also:
- [C2 Profile Definition](./references/c2-profile-definition.md) - If building a custom C2 profile
- [Container Syncing](./references/container-syncing.md) - How containers register with Mythic

## Reference Index

For detailed documentation on each topic, consult the following pages. Load only the pages you need to conserve context.

**Full index**: [Reference Index](./references/index.md)

### Quick Reference

| Topic | Reference | When to Use |
|-------|-----------|-------------|
| Project structure | [Project Layout](./references/project-layout.md) | Setting up the repo/container |
| Agent definition | [Payload Type Definition](./references/payload-type-definition.md) | Defining the agent class and build |
| Wire format | [Agent Message Format](./references/agent-message-format.md) | Implementing message encoding |
| First contact | [Initial Checkin](./references/initial-checkin.md) | Implementing checkin + key exchange |
| Fetch tasks | [Get Tasking](./references/get-tasking.md) | Implementing the task loop |
| Return output | [Post Response](./references/post-response.md) | Sending task results |
| Download files | [File Downloads](./references/file-downloads.md) | Agent -> Mythic file transfer |
| Upload files | [File Uploads](./references/file-uploads.md) | Mythic -> Agent file transfer |
| Command defs | [Commands](./references/commands.md) | Defining commands and parameters |
| Task processing | [Create Tasking](./references/create-tasking.md) | Server-side task preprocessing |
| OPSEC gates | [OPSEC Checking](./references/opsec-checking.md) | Pre/post task OPSEC checks |
| Custom format | [Translation Containers](./references/translation-containers.md) | Non-JSON / custom crypto |
| C2 profiles | [C2 Profile Definition](./references/c2-profile-definition.md) | Building a custom C2 profile |
| SOCKS proxy | [SOCKS](./references/socks.md) | SOCKS5 tunneling through agent |
| Reverse port fwd | [Reverse Port Forward](./references/rpfwd.md) | Reverse port forwarding through agent |
| P2P mesh | [P2P Connections](./references/p2p-connections.md) | Peer-to-peer agent linking |
| Sync lifecycle | [Container Syncing](./references/container-syncing.md) | Understanding container registration |
