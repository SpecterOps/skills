# OWASP Input Validation

Use this reference when reviewing any data that crosses a trust boundary. Validate early, on the server, at both syntactic and semantic levels.

## Review Checks

- Identify every untrusted source: HTTP input, files, queue messages, partner feeds, webhooks, database reads from lower-trust stores, and environment/config values.
- Check type conversion, length limits, ranges, enum allowlists, full-string regex anchoring, normalization, and Unicode handling.
- Verify semantic rules such as `start_date <= end_date`, positive amounts, allowed state transitions, and tenant ownership.
- Treat denylist filtering as supplemental only. It must not replace allowlists for structured data.
- Confirm validation happens before persistence, rendering, command execution, path construction, or policy decisions.

## Pattern Examples

### Client-side only validation

```ts
// Vulnerable: browser checks are bypassable.
const role = req.body.role;
await users.create({ email: req.body.email, role });
```

```ts
// Safer: enforce allowed values on the server.
const role = String(req.body.role);
if (!["member", "viewer"].includes(role)) {
  throw new BadRequest("invalid role");
}
await users.create({ email: validateEmail(req.body.email), role });
```

### Denylist instead of allowlist

```python
# Vulnerable: misses alternate encodings and legitimate cases.
if "<script>" in comment or "1=1" in comment:
    reject()
```

```python
# Safer: validate the field shape, then encode for the eventual sink.
comment = normalize_text(request.json["comment"])
if len(comment) > 2000:
    raise BadRequest("comment too long")
```

### Missing semantic validation

```python
# Vulnerable: dates parse, but the business rule is unchecked.
start = parse_date(body["start"])
end = parse_date(body["end"])
create_booking(start, end)
```

```python
start = parse_date(body["start"])
end = parse_date(body["end"])
if end < start:
    raise BadRequest("end must not precede start")
create_booking(start, end)
```

## Review Prompts

- Which inputs are accepted because the client UI normally constrains them?
- Does the code normalize before comparison and authorization?
- Are regexes anchored and bounded, or can they trigger ReDoS?
- Are free-form text fields handled with sink-specific output encoding rather than over-aggressive filtering?
- Do file and archive inputs get size, path, type, and decompression checks?

## Source

Local summary based on the OWASP Input Validation Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html`
