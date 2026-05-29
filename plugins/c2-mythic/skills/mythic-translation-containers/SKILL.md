---
name: mythic-translation-containers
description: Develop Mythic translation containers for custom agent wire formats, custom encryption/decryption, and Mythic-to-agent message conversion. Use when a payload type sets translation_container, when mythic_encrypts is false with custom crypto, or when a C2 profile/agent needs non-JSON or binary message formats.
metadata:
  author: "GhostWorks"
---

# Mythic Translation Containers

## Scope

Use this skill when the main artifact is a Mythic translation container rather than an implant or C2 profile. Translation containers convert between Mythic's internal C2 message model and a custom agent wire format, and can generate or manage cryptographic keys for payload builds.

Use `$mythic-profiles` for listener/transport container work. Use `$mythic-implant-development` for payload type and agent command implementation.

## Workflow

1. **Decide whether translation is required**
   - Required when the agent wire format is not Mythic's default JSON message format.
   - Required when custom crypto is used with `mythic_encrypts = False`.
   - Useful when multiple profiles/agents share a binary or service-specific envelope.

2. **Wire payload type to translation container**
   - Set `translation_container = "<container_name>"` in the payload type definition.
   - Ensure container name is lowercase-safe for Docker image naming.
   - Keep the container name stable; payload types and installed services depend on it.

3. **Implement required translation functions**
   - Generate keys for selected crypto parameters.
   - Translate Mythic -> custom agent format.
   - Translate custom agent format -> Mythic.
   - Keep conversion deterministic and side-effect free where possible.

4. **Coordinate crypto responsibilities**
   - If Mythic encrypts (`mythic_encrypts=True`), translation can focus on serialization/envelope conversion.
   - If custom crypto is used, translation handles decrypt/verify and encrypt/sign operations.
   - Do not log generated keys, decrypted task contents, or full plaintext messages.

5. **Validate round trips**
   - Unit test translation both directions with sample messages.
   - Build a payload using the associated payload type and C2 profile.
   - Confirm checkin, get-tasking, post-response, and file transfer paths.
   - Test bad input: malformed envelope, bad MAC/signature, unknown action, and unsupported crypto choice.

## Reference loading

- Read `references/translation-workflow.md` for implementation patterns and validation cases.
- Read `../mythic-implant-development/references/translation-containers.md` for local detailed examples.
- Read `../mythic-implant-development/references/agent-message-format.md` when converting Mythic messages to/from wire messages.
- Read `../mythic-profiles/references/profile-development.md` if the translation is profile-specific.

## Output requirements

For implementation/review tasks, return:

- associated payload type(s) and C2 profile(s)
- container name and language/runtime
- crypto responsibility split
- message envelope schema
- functions/files changed
- validation samples and expected outputs
- security notes for key handling and logging
