# Project Layout

This page describes the required project structure for a Mythic agent, including Docker containers, folder layout, and entry points.

Source: https://docs.mythic-c2.net/customizing/payload-type-development

## Architecture Overview

Mythic uses Docker containers for all agents and C2 profiles. Your agent lives in its own container that connects to Mythic via RabbitMQ and gRPC. The container:

- Syncs metadata about the payload type (Python classes or Go structs)
- Contains the agent source code (whatever language your agent is in)
- Runs the build function when an operator creates a payload
- Syncs command metadata and definitions
- Runs create_tasking and other server-side processing

## Repository Format (External Agent Template)

All installable agents follow the External Agent format: https://github.com/MythicMeta/Mythic_External_Agent

```
your-agent-repo/
  Payload_Type/
    your_agent_name/          # This entire folder goes into Mythic/InstalledServices/
      Dockerfile              # REQUIRED - builds the container image
      main.py                 # Python entry point (or main.go + Makefile for Go)
      your_agent_name/
        mythic/
          agent_functions/
            builder.py        # PayloadType class definition + build function
            command1.py       # Command definitions
            command2.py
            ...
          browser_scripts/    # Optional JavaScript browser scripts
        agent_code/           # Your actual agent source code
          ...
  C2_Profiles/                # Optional - if shipping a custom C2 profile
    your_c2_name/
      ...
  documentation-docker/       # Optional - Hugo documentation
  config.json                 # Marks sections to exclude from install
  agent_capabilities.json     # Agent feature matrix for the overview page
```

## Important Naming Rules

- Docker does not allow capital letters in container names
- Use only: lowercase letters, numbers, and underscores
- The folder name in `InstalledServices` becomes the Docker image/container name
- It does not have to match the agent name in code, but it helps

## Dockerfile

The Dockerfile is the only file that **MUST** exist. Mythic provides base images:

| Base Image | Contents |
|-----------|----------|
| `itsafeaturemythic/mythic_python_base:latest` | Python 3.11 + `mythic_container` PyPi package |
| `itsafeaturemythic/mythic_go_base:latest` | GoLang 1.25 |
| `itsafeaturemythic/mythic_python_go:latest` | Python 3.11 + `mythic_container` + GoLang 1.25 |
| `itsafeaturemythic/mythic_go_dotnet:latest` | GoLang 1.25 + .NET SDK |
| `itsafeaturemythic/mythic_go_macos:latest` | GoLang 1.25 + macOS SDK |
| `itsafeaturemythic/mythic_python_macos:latest` | Python 3.11 + `mythic_container` + macOS SDK |

**CRITICAL: Build environment constraint** - The payload type's `build` function runs INSIDE this container. Docker is NOT available inside the container. All compilers, toolchains, and build tools your agent needs must be installed in the Dockerfile via `RUN` commands. You cannot use `docker build`, `docker run`, or any Docker commands from within the build function.

### Python Dockerfile Example

```dockerfile
FROM itsafeaturemythic/mythic_python_base:latest

# Install additional build dependencies for your agent's compilation
# These tools will be available to the build() function at payload generation time
RUN pip install some-python-module
RUN apt-get install -y some-tool

WORKDIR /Mythic/

CMD ["python3", "main.py"]
```

### GoLang Dockerfile Example

```dockerfile
FROM itsafeaturemythic/mythic_go_base:latest

WORKDIR /Mythic/

COPY [".", "."]

RUN make build

CMD make run
```

### Example: Adding a Non-Default Toolchain

If your agent is written in a language not provided by the base images, install it in the Dockerfile:

```dockerfile
FROM itsafeaturemythic/mythic_python_base:latest

# Install Rust toolchain for a Rust-based agent
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install MinGW for cross-compiling C/C++ to Windows
RUN apt-get update && apt-get install -y mingw-w64

WORKDIR /Mythic/

CMD ["python3", "main.py"]
```

The `build()` function can then call these tools via `subprocess.run()` (Python) or `os/exec` (Go) to compile the agent.

## Volume Mapping

The `Mythic/InstalledServices/[agent name]` folder on the host is mapped to `/Mythic` inside the container. Edits on disk appear inside the container and vice versa.

For Go containers, this means the compiled binary must be copied outside the mapped directory during build (to `/` for example) and copied back at runtime, because the volume mount replaces the build output.

## Entry Points

### Python: main.py

```python
import mythic_container
import asyncio
# Import your agent's definition modules so they register
import your_agent_name

mythic_container.mythic_service.start_and_run_forever()
```

The agent functions directory must contain an `__init__.py` (or equivalent imports) so Python discovers the PayloadType class and Command classes.

Any code changes are immediately reflected in the container. Restart with: `sudo ./mythic-cli start [agent_name]`

### GoLang: main.go + Makefile

```go
package main

import (
    agentfunctions "YourModule/your_agent_name/agentfunctions"
    "github.com/MythicMeta/MythicContainer"
)

func main() {
    agentfunctions.Initialize()
    MythicContainer.StartAndRunForever([]MythicContainer.MythicServices{
        MythicContainer.MythicServicePayload,
    })
}
```

#### Makefile

```makefile
BINARY_NAME?=main

build:
	go mod tidy
	go build -o ${BINARY_NAME} .
	cp ${BINARY_NAME} /

run:
	cp /${BINARY_NAME} .
	./${BINARY_NAME}
```

Note: The binary is copied to `/` during build and back to the working directory at run time. This is because the source directory is volume-mapped and would overwrite the built binary.

## Installation and Testing

### Manual steps (what `mythic-cli install` does automatically):

1. Copy agent folder to `Mythic/InstalledServices/`
2. Register with docker-compose: `sudo ./mythic-cli add your_agent_name`
3. Build the image: `sudo ./mythic-cli build your_agent_name`
4. Start the container: `sudo ./mythic-cli start your_agent_name`
5. Check logs: `sudo ./mythic-cli logs your_agent_name`

### Local development without Docker

Create a `rabbitmq_config.json` in your agent's root directory:

```json
{
  "rabbitmq_host": "127.0.0.1",
  "rabbitmq_password": "<from Mythic/.env>",
  "mythic_server_host": "127.0.0.1",
  "mythic_server_grpc_port": 17444,
  "debug_level": "debug",
  "rabbitmq_port": 5432
}
```

For remote development, ensure:
- `MYTHIC_RABBITMQ_LISTEN_LOCALHOST_ONLY` is set to `false`
- The RabbitMQ password is shared to your remote host

## Making the Agent Installable

For `mythic-cli install github.com/YourOrg/your-agent` to work:

1. Follow the External Agent repo format above
2. Include a `config.json` to mark sections to exclude
3. Optionally add `agent_capabilities.json` for the overview matrix page

## agent_capabilities.json

```json
{
  "os": ["Windows", "Linux", "macOS"],
  "languages": ["Go"],
  "features": {
    "mythic": {
      "checkin": true,
      "get_tasking": true,
      "post_response": true,
      "file_download": true,
      "file_upload": true,
      "socks": false,
      "rpfwd": false,
      "p2p": false,
      "interactive": false,
      "process_browser": false,
      "file_browser": false
    },
    "custom": ["feature1", "feature2"]
  },
  "payload_output": ["exe", "bin"],
  "architectures": ["AMD_x64", "ARM_x64"],
  "c2": ["http"],
  "supported_wrappers": [],
  "mythic_version": "3.3",
  "agent_version": "1.0.0"
}
```
