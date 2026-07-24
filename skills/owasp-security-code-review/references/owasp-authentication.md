# OWASP Authentication

Use this reference when reviewing login, password change, password recovery, MFA, sensitive actions, identity proofing, or credential storage and comparison.

## Review Checks

- Confirm sensitive internal or backend accounts cannot authenticate through public frontends.
- Check password policy for adequate minimum length, long passphrase support, no silent truncation, and breached-password blocking.
- Verify password comparison uses framework/library primitives with constant-time behavior where relevant.
- Require current credentials or equivalent re-authentication before changing passwords, email addresses, payment details, or trusted devices.
- Trigger re-authentication after password resets, account recovery, suspicious activity, or other high-risk events.
- Keep login and authenticated traffic on TLS and avoid account-enumerating responses.

## Pattern Examples

### Account enumeration

```ts
// Vulnerable
if (!user) return res.status(404).json({ error: "user not found" });
if (!verify(password, user.hash)) return res.status(401).json({ error: "wrong password" });
```

```ts
// Safer
if (!user || !verify(password, user.hash)) {
  return res.status(401).json({ error: "invalid credentials" });
}
```

### Password change without re-authentication

```python
# Vulnerable
@app.post("/account/password")
def change_password(user, body):
    users.set_password(user.id, body["new_password"])
```

```python
@app.post("/account/password")
def change_password(user, body):
    if not verify_password(body["current_password"], user.password_hash):
        raise Unauthorized("reauthentication required")
    users.set_password(user.id, validate_new_password(body["new_password"]))
    sessions.invalidate_all(user.id)
```

### Unsafe password comparison

```php
// Vulnerable
if ($storedHash == hash("sha256", $_POST["password"])) { ... }

// Safer
if (password_verify($_POST["password"], $storedHash)) { ... }
```

## Review Prompts

- Can error messages, timing, or recovery flows reveal whether an account exists?
- Do sensitive actions require fresh authentication rather than only an old session?
- Are password reset and recovery artifacts single-use, time-limited, and invalidated after success?
- Are authentication state changes followed by session rotation or invalidation?

## Source

Local summary based on the OWASP Authentication Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html`
