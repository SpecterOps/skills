# OWASP Session Management

Use this reference when reviewing session IDs, cookies, token exchange, session storage, logout, fixation, timeout, and privilege transitions.

## Review Checks

- Treat a session ID as equivalent to the authenticated user's strongest credential for the lifetime of the session.
- Require cryptographically random, meaningless identifiers with adequate entropy.
- Keep server-side state out of the client-visible session ID unless using a separately reviewed signed/encrypted token design.
- Prefer cookie-based session exchange and reject session IDs from URLs or alternate channels when cookies are expected.
- Set `Secure`, `HttpOnly`, and appropriate `SameSite` attributes.
- Rotate session IDs after login, password changes, role changes, and other privilege transitions.
- Invalidate sessions on logout, timeout, password reset, account disablement, and re-authentication events.

## Pattern Examples

### Predictable session ID

```python
# Vulnerable
session_id = f"{user.id}-{int(time.time())}"
```

```python
# Safer
session_id = secrets.token_urlsafe(32)
session_store.put(session_id, {"user_id": user.id})
```

### Session ID in URL

```html
<!-- Vulnerable: leaks into history, logs, and referrers -->
<a href="/account?sid=abc123">Account</a>
```

```http
Set-Cookie: id=<opaque-token>; Secure; HttpOnly; SameSite=Lax; Path=/
```

### Missing rotation after login

```ts
// Vulnerable: anonymous session survives privilege change.
req.session.userId = user.id;
```

```ts
// Safer
await regenerateSession(req);
req.session.userId = user.id;
```

## Review Prompts

- Is any part of the token predictable, meaningful, or user-controlled?
- Are session IDs accepted through query strings, form fields, headers, or cookies?
- Does the app rotate IDs at every privilege boundary?
- Are old sessions invalidated after password reset, account recovery, or logout?
- Can XSS, mixed HTTP/HTTPS, or missing cookie flags expose the token?

## Source

Local summary based on the OWASP Session Management Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html`
