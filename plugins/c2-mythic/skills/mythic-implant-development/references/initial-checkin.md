# Initial Checkin

This page describes all methods for an agent to perform its initial checkin with Mythic, including key exchange protocols.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/create_tasking/agent-side-coding/initial-checkin

## UUID Lifecycle

All UUIDs are UUIDv4 format (36 chars): `b446b886-ab97-49b2-b240-969a75393c06`

The goal of checkin is to go from a **payloadUUID** to a **callbackUUID**:

1. Agent starts with a payloadUUID (embedded at build time)
2. Checkin exchanges this for a callbackUUID
3. All subsequent messages use the callbackUUID

If a callback sends a checkin message more than once, Mythic uses it to update callback info rather than creating a new callback.

## Plaintext Checkin

Used for testing or when C2 profile crypto parameter is set to `none`.

### Agent -> Mythic

```json
Base64( PayloadUUID + JSON({
    "action": "checkin",
    "uuid": "payload uuid",           // required

    "ips": ["127.0.0.1"],             // optional
    "os": "macOS 10.15",              // optional
    "user": "its-a-feature",          // optional
    "host": "spooky.local",           // optional
    "pid": 4444,                      // optional
    "architecture": "x64",            // optional
    "domain": "test",                 // optional
    "integrity_level": 3,             // optional (1=low, 2=medium, 3=high, 4=SYSTEM)
    "external_ip": "8.8.8.8",        // optional
    "encryption_key": "base64 key",   // optional
    "decryption_key": "base64 key",   // optional
    "process_name": "osascript"       // optional
})
)
```

**integrity_level values:**
- 1 = Low integrity (Windows) / restricted user (Linux)
- 2 = Medium integrity / standard user
- 3 = High integrity / sudoer
- 4 = SYSTEM / root

### Mythic -> Agent

```json
Base64( PayloadUUID + JSON({
    "action": "checkin",
    "id": "callbackUUID",
    "status": "success"
})
)
```

After this, the agent uses the new `callbackUUID` for all messages.

## Static AES256 Encryption Checkin

Uses a per-payload AES256 key generated at build time. The key is produced when the C2 profile has a parameter with `crypto_type=True` set to `aes256_hmac`.

The base64-encoded 32-byte key is passed to the agent during the build process.

### Agent -> Mythic

```json
Base64( PayloadUUID + AES256(
    JSON({
        "action": "checkin",
        "uuid": "payload uuid",           // required
        "ips": ["127.0.0.1"],             // optional
        "os": "macOS 10.15",              // optional
        "user": "its-a-feature",          // optional
        "host": "spooky.local",           // optional
        "pid": 4444,                      // optional
        "architecture": "x64",            // optional
        "domain": "test",                 // optional
        "integrity_level": 3,             // optional
        "external_ip": "8.8.8.8",        // optional
        "encryption_key": "base64 key",   // optional
        "decryption_key": "base64 key",   // optional
        "process_name": "osascript"       // optional
    })
)
)
```

### Mythic -> Agent

```json
Base64( PayloadUUID + AES256(
    JSON({
        "action": "checkin",
        "id": "callbackUUID",
        "status": "success"
    })
)
)
```

After this, the agent uses the callbackUUID as the outer UUID but continues using the same static AES key.

## RSA Encrypted Key Exchange (EKE)

Provides forward secrecy by negotiating a per-session AES key. This is a 3-message exchange.

### Message 1: Agent -> Mythic (Staging)

Agent generates a 4096-bit RSA keypair in memory and sends the public key:

```json
Base64( PayloadUUID + AES256(
    JSON({
        "action": "staging_rsa",
        "pub_key": "base64 of public RSA key",
        "session_id": "20char random string"
    })
)
)
```

- Encrypted with the initial AESPSK from build time
- `pub_key` can be the full PEM (including BEGIN/END blocks) base64-encoded, or just the base64 data between the PEM markers
- `session_id` is a 20-character random string to correlate staging messages

### Message 2: Mythic -> Agent (Session Key)

```json
Base64( PayloadUUID + AES256(
    JSON({
        "action": "staging_rsa",
        "uuid": "tempUUID",
        "session_key": Base64( RSAPub( new_aes_session_key ) ),
        "session_id": "same 20char string"
    })
)
)
```

- Encrypted with the same initial AESPSK
- `session_key` is a new AES256 key encrypted with the agent's RSA public key, then base64-encoded
- `uuid` is a temporary staging UUID for the next message

### Message 3: Agent -> Mythic (Checkin with New Key)

```json
Base64( tempUUID + AES256_NEW_KEY(
    JSON({
        "action": "checkin",
        "uuid": "payload uuid",
        // ... all standard checkin fields
    })
)
)
```

- Uses the **tempUUID** as the outer UUID
- Encrypted with the **new negotiated AES session key**
- Inner `uuid` is still the original payloadUUID

### Message 4: Mythic -> Agent (Callback UUID)

```json
Base64( tempUUID + AES256_NEW_KEY(
    JSON({
        "action": "checkin",
        "id": "callbackUUID",
        "status": "success"
    })
)
)
```

From here on, the agent uses the **callbackUUID** and the **negotiated AES key** for all messages.

## Custom EKE (via Translation Container)

For completely custom key exchange protocols, use a translation container.

### Flow

1. Agent sends: `Base64( payloadUUID + customMessage )`
2. Mythic looks up the payload, finds a translation container
3. Mythic calls `translate_from_c2_format` with:

```json
{
    "enc_key": null,
    "dec_key": null,
    "uuid": "uuid from message",
    "profile": "c2 profile name",
    "mythic_encrypts": true,
    "type": null,
    "message": "base64 of the raw message"
}
```

4. Instead of returning a `checkin` action, return `staging_translation`:

```json
{
    "action": "staging_translation",
    "session_id": "random session id",
    "enc_key": "<raw bytes of encryption key for next message>",
    "dec_key": "<raw bytes of decryption key for next message>",
    "crypto_type": "your crypto type identifier",
    "next_uuid": "UUID for front of next message",
    "message": "<raw bytes to send back to agent>"
}
```

5. This repeats as many times as needed until you return an actual `checkin` action.

For persistent storage between staging messages, use:
- `create_agentstorage(unique_id, data)` - store arbitrary bytes
- `get_agentstorage(unique_id)` - retrieve stored data
- `delete_agentstorage(unique_id)` - clean up

## AES256 Encryption Details

All AES256 encryption in Mythic uses:

- **Algorithm**: AES-256
- **Mode**: CBC
- **Padding**: PKCS7, block size 16
- **IV**: 16 random bytes, generated per message
- **Key**: 32 bytes (256 bits)
- **Wire format**: `IV (16 bytes) + Ciphertext + HMAC`
- **HMAC**: SHA-256 using the same AES key, computed over `IV + Ciphertext`

### Implementation Pseudocode

```
encrypt(plaintext, key):
    iv = random_bytes(16)
    padded = pkcs7_pad(plaintext, 16)
    ciphertext = aes_cbc_encrypt(padded, key, iv)
    hmac = hmac_sha256(key, iv + ciphertext)
    return iv + ciphertext + hmac

decrypt(blob, key):
    iv = blob[0:16]
    hmac_received = blob[-32:]
    ciphertext = blob[16:-32]
    hmac_computed = hmac_sha256(key, iv + ciphertext)
    assert hmac_received == hmac_computed
    padded = aes_cbc_decrypt(ciphertext, key, iv)
    return pkcs7_unpad(padded)
```

## RSA Encryption Details

- **Algorithm**: RSA
- **Padding**: PKCS1_OAEP with SHA-1
- **Key size**: 4096 bits
