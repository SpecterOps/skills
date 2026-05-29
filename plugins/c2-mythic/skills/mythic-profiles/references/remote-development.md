# Mythic Profile Remote Development

Use this reference when iterating on C2 profiles outside a production Mythic deployment.

## Development loop

1. Work in the profile repository or `Mythic/InstalledServices/<profile>` checkout.
2. Keep profile metadata, server code, and documentation in the profile folder.
3. Register/add the container with Mythic using the installed service workflow.
4. Start only the profile container while iterating when possible.
5. Watch profile container logs and Mythic UI sync state.
6. Rebuild/restart after metadata, dependency, or server-binary changes.
7. Build a test payload that supports the profile and exercise checkin/tasking.

## Local/remote split

When the editor is local and Mythic is remote:

- Use a synchronized checkout or remote development session.
- Keep secrets and operator-specific hosts out of committed defaults.
- Document which Mythic instance, profile container, and payload type are used for validation.
- Prefer replayable validation commands and config snippets over screenshots-only evidence.

## Container iteration checklist

- Profile folder name and C2Profile `name` are consistent.
- Container name is lowercase-safe for Docker image naming.
- `server_binary_path` exists and is executable for egress profiles.
- `server_folder_path` contains expected config/server files.
- Parameter defaults are safe for development and obvious to change.
- Profile starts cleanly after `mythic-cli start <profile>`.
- Payload build UI shows the new/changed profile parameters.
