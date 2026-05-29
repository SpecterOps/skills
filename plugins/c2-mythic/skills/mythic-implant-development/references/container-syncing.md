# Container Syncing

This page describes how Mythic containers register and synchronize their definitions.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/payload-type-info/container-syncing

## What Is Syncing

When a container starts, it connects to RabbitMQ and sends a JSON representation of everything about the payload type:
- Payload type metadata (name, OS, parameters, etc.)
- All command definitions and their parameters
- Build parameters
- Browser scripts
- Everything needed for Mythic to present the agent in the UI

## When Does Syncing Happen

### Container startup
When a payload container starts, it immediately sends its sync data to Mythic.

### New container detected
If Mythic receives a connection from a container it doesn't recognize, it requests a sync.

### C2 profile sync cascade
When a C2 profile syncs, it triggers a re-sync of ALL payload type containers. This is because a payload type might declare support for a C2 profile that hasn't started yet. When that C2 profile comes online, all payload types need to re-register so the UI properly shows the supported C2 options.

### Wrapper sync cascade
When a wrapper payload type syncs, it triggers a re-sync of all non-wrapper payload types. A payload type might support a wrapper that hasn't started yet, so when the wrapper comes online, everything re-syncs.

## Development Implications

- Changes to command definitions, parameters, or agent metadata take effect after container restart
- For Python containers: `sudo ./mythic-cli start [agent_name]` restarts and triggers re-sync
- For Go containers: rebuild first (`make build`), then restart
- Syncing is automatic - no manual registration needed
- The UI updates immediately after a successful sync

## Checking Sync Status

- Container appears in the Mythic UI under Payload Types
- Check container logs: `sudo ./mythic-cli logs [agent_name]`
- If sync fails, errors appear in the event feed

## Version Tracking

Latest container/PyPi versions are tracked on the Mythic GitHub README: https://github.com/its-a-feature/Mythic
