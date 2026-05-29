# Mythic C2 Profile Development Reference

## Profile package anatomy

A Mythic C2 profile normally includes:

- profile definition code containing the `C2Profile` metadata and parameters
- container build material such as Dockerfile or project metadata
- server binary/script for egress profiles
- server folder files such as config templates, redirect rules, static assets, or scripts
- optional profile icon and documentation

For repositories modeled like MythicC2Profiles, inspect the existing profile folders first and follow their language/container conventions.

## Egress profile data flow

```text
agent transport message
  -> profile listener/server
  -> extract Mythic agent message
  -> POST to Mythic /agent_message
  -> receive Mythic response
  -> wrap/encode response for transport
  -> agent
```

Implementation notes:

- Keep the transport parsing layer separate from Mythic forwarding code.
- Make bind host, bind port, callback host, URI paths, headers, and TLS material explicit parameters.
- Fail closed on malformed messages; log enough for debugging without printing keys or full task data.
- Add clear startup validation for missing config values, invalid ports, or inaccessible certificate/key files.

## P2P profile data flow

P2P profiles usually do not run a listener container. They define operator parameters and agent-side routing metadata for links such as TCP, SMB, or custom peer channels.

Implementation notes:

- Set `is_p2p=True`.
- Keep parameters focused on peer addressing, pipe names, listen/connect mode, and routing labels.
- Validate that agent code emits delegate messages with the correct `c2_profile` name.

## Parameter design checklist

- Stable `name` values; changing names can break payload builders and saved configs.
- Useful `description` text for operators.
- Safe `default_value` values; avoid environment-specific secrets.
- `verifier_regex` for URLs, ports, UUIDs, pipe names, and profile-specific syntax.
- `required=True` for values needed at build or runtime.
- `randomized=True` plus `format_string` for per-payload identifiers.
- `crypto_type=True` only for parameters Mythic should use to generate/store crypto material.
- Dictionary parameters for HTTP headers or metadata maps.
- Array parameters for lists of URIs, domains, or failover hosts.

## Validation checklist

1. Container builds successfully.
2. Container starts and syncs profile metadata into Mythic.
3. Profile is selectable in payload build UI.
4. Payload type declares support for the profile.
5. Payload build receives selected parameter values.
6. Agent can check in through the profile.
7. Agent can get tasking and post responses.
8. File upload/download paths work if supported by the agent/profile transport.
9. Restarting the profile container preserves expected config behavior.
10. Error logs are actionable and do not expose secrets.

## Common mistakes

- Using a profile `name` that does not match payload type supported C2 entries.
- Forgetting `server_binary_path` for egress profiles.
- Marking a listener profile as `is_p2p=True`.
- Logging full encrypted/decrypted messages or generated keys.
- Embedding operator-selected C2 parameters in the agent with mismatched field names.
- Adding profile parameters but not updating the payload build function to consume them.
