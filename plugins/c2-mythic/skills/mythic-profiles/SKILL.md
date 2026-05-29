---
name: mythic-profiles
description: Develop Mythic C2 profiles/listeners and transport containers. Use when designing, implementing, modifying, or validating Mythic C2 profile repositories like MythicC2Profiles, including HTTP/DNS/WebSocket/TCP/SMB-style egress or P2P profiles, C2Profile parameters, server binaries, redirector material, OPSEC checks, and payload-type integration.
metadata:
  author: "GhostWorks"
---

# Mythic Profiles

## Scope

Use this skill for Mythic C2 profile development: profile container layout, `C2Profile` definitions, parameter modeling, listener/server implementation, P2P versus egress profile decisions, and integration with Mythic payload types.

Use `$mythic-implant-development` instead when the primary task is implementing an agent/payload type or agent commands. Use this skill when the primary artifact is a C2 profile/listener/transport.

## Workflow

1. **Classify the profile**
   - Egress profile: server-side code receives agent traffic and forwards to Mythic `/agent_message`.
   - P2P profile: no listening server; parameters define agent-to-agent connection details.
   - Translation-aware profile: coordinate with a translation container if wire format or crypto differs from Mythic messages.

2. **Set up the development loop**
   - Read `references/remote-development.md` when the task involves local/remote Mythic development, container iteration, or installed-service workflow.
   - Confirm profile folder name, C2Profile `name`, and Mythic installed service name align.
   - Use focused container restarts and payload-build smoke tests during iteration.

3. **Inspect the repository shape**
   - Identify profile language, Docker/container entrypoint, profile definition file, server binary/script, config templates, and any profile-specific utilities.
   - For MythicC2Profiles-style work, treat each top-level profile as a standalone container package.
   - Preserve existing profile naming, parameter names, and build/deploy conventions unless the user asks for a migration.

4. **Define or update profile metadata**
   - `name`: stable profile identifier used by payload types.
   - `description`, `author`, `semver`.
   - `is_p2p`: `False` for listener/egress profiles, `True` for P2P profiles.
   - `server_binary_path`: executable/script that handles traffic for egress profiles.
   - `server_folder_path`: folder exposed in Mythic UI for server-side files/config.

5. **Model C2 parameters**
   - Include operator-facing parameters such as callback host/port, interval, jitter, headers, bind address, URI paths, proxy settings, or peer connection fields.
   - Use `verifier_regex` for format-sensitive values.
   - Use `crypto_type=True` for Mythic-managed crypto parameters such as AES/HMAC profile keys.
   - Prefer parameter names the payload build function can consume directly through `get_parameters_dict()`.

6. **Implement listener/server behavior**
   - Accept or receive the profile transport format.
   - Extract the Mythic agent message.
   - Forward to Mythic’s `/agent_message` endpoint.
   - Return Mythic’s response in the profile’s transport format.
   - Add bounded config validation, useful logs, and no secret-bearing debug output.

7. **Integrate with payload types**
   - Ensure payload types list the profile name in `c2_profiles` / supported C2 profiles.
   - Confirm the build function embeds or serializes selected profile parameters into agent configuration.
   - Keep agent wire format and profile server expectations synchronized.

8. **Validate**
   - Confirm container starts and syncs with Mythic.
   - Confirm profile appears in payload build UI.
   - Build a test payload with the profile selected.
   - Confirm checkin, get-tasking, post-response, file transfer, and error paths as applicable.
   - Document exact commands, config values changed, and validation evidence.

## Reference loading

Read only what is needed:

- `references/developer-series.md` for routing based on the Mythic for Developers playlist topics.
- `references/profile-development.md` for implementation patterns, profile file anatomy, and validation checklist.
- `references/remote-development.md` for local/remote container iteration and installed-service workflow.
- `references/third-party-service-profiles.md` for profiles that broker traffic through external services such as chat/storage/webhook APIs.
- `../mythic-implant-development/references/c2-profile-definition.md` for detailed `C2Profile` class and parameter examples.
- `../mythic-implant-development/references/agent-message-format.md` when the transport wraps Mythic agent messages.
- `$mythic-translation-containers` when profile behavior depends on custom message formats or crypto.
- `../mythic-implant-development/references/p2p-connections.md` for SMB/TCP-style P2P routing.

## Output requirements

For design/review tasks, return:

- profile type: egress, P2P, or translation-aware
- files changed or files to create
- parameter schema and operator-visible defaults
- server/listener data flow
- payload-type integration points
- validation commands/checks
- risks, assumptions, and unresolved profile-specific questions
