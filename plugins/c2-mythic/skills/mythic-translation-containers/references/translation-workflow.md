# Mythic Translation Container Workflow

## Container responsibilities

A translation container handles fast message conversion for a payload type. It differs from payload type and C2 profile containers because it uses low-latency request/response translation rather than long-running RabbitMQ jobs.

Core responsibilities:

1. Generate encryption/decryption keys when Mythic asks for them.
2. Convert Mythic messages to the custom agent/C2 wire format.
3. Convert custom agent/C2 wire messages back to Mythic's internal message structure.

## Python implementation shape

- Define a subclass of `TranslationContainer`.
- Set `name`, `description`, and `author`.
- Implement key generation.
- Implement translate-to-custom and translate-from-custom functions.
- Start the service with Mythic container service startup code.

## Go implementation shape

- Define a `translationstructs.TranslationContainer` value.
- Set `Name`, `Description`, `Author`.
- Provide `GenerateEncryptionKeys`, `TranslateMythicToCustomFormat`, and `TranslateCustomToMythicFormat` handlers.
- Register with `AllTranslationData` during initialization.
- Start translation services through MythicContainer service startup.

## Message design checklist

- Version field for future migrations.
- Action/message type field.
- Payload UUID/callback UUID handling.
- Nonce/IV and MAC/signature fields when custom crypto is used.
- Compression flag if using compression.
- Chunk metadata for file transfer.
- Explicit encoding: raw bytes, base64, JSON, protobuf, msgpack, etc.

## Security checklist

- Reject malformed messages before parsing deeply.
- Verify MAC/signature before decrypting or trusting fields.
- Use constant-time comparisons for authentication tags when applicable.
- Never log plaintext tasking, response bodies, or keys.
- Validate crypto parameter choices and fail closed on unknown values.
- Keep deterministic test vectors in references/tests, not production secrets.

## Validation cases

| Case | Expected result |
|---|---|
| valid checkin | converts to Mythic checkin message |
| valid tasking response | converts custom response to Mythic response |
| valid Mythic task | converts Mythic task to custom wire format |
| bad envelope version | failure with actionable error |
| missing UUID | failure before forwarding |
| bad MAC/signature | failure, no plaintext logging |
| unsupported crypto mode | failure during key generation or build validation |
| max-size payload | chunking or bounded failure |
