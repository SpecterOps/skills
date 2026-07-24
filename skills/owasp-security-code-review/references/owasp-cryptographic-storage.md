# OWASP Cryptographic Storage

Use this reference when reviewing data-at-rest encryption, key handling, IVs/nonces, token generation, password storage decisions, or custom cryptographic code.

## Review Checks

- Start from the threat model and determine which layer must protect the asset.
- Avoid storing sensitive data when the application can avoid it.
- Use maintained libraries and standard algorithms rather than custom cryptography.
- Prefer authenticated encryption modes such as GCM or CCM.
- Use cryptographically secure randomness for keys, nonces, IVs, session IDs, and recovery tokens.
- Keep keys separate from ciphertext and define generation, rotation, revocation, backup, and access controls.
- Do not use reversible encryption for password storage.

## Pattern Examples

### Static key and ECB mode

```python
# Vulnerable
KEY = b"0123456789abcdef"
cipher = AES.new(KEY, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(secret, 16))
```

```python
# Safer
key = key_manager.get_data_key("customer-records")
nonce = secrets.token_bytes(12)
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(secret)
```

### Predictable token generation

```ts
// Vulnerable
const resetToken = Math.random().toString(36).slice(2);
```

```ts
// Safer
const resetToken = crypto.randomBytes(32).toString("base64url");
```

### Encrypting passwords

```python
# Vulnerable
stored_password = aes_encrypt(user_password, key)
```

```python
# Safer
stored_password = password_hasher.hash(user_password)
```

## Review Prompts

- What attacker is the encryption intended to stop: stolen disk, DB dump, service compromise, or operator misuse?
- Is confidentiality paired with integrity and authenticity?
- Are nonces or IVs unique for each encryption operation?
- Are keys stored, rotated, and revoked independently from the encrypted data?
- Does any custom crypto or disabled certificate validation bypass the library's security guarantees?

## Source

Local summary based on the OWASP Cryptographic Storage Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html`
