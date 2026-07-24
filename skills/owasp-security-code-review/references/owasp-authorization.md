# OWASP Authorization

Use this reference when reviewing role checks, object ownership, tenant isolation, IDOR, admin actions, static resources, background jobs, and policy-engine integration.

## Review Checks

- Separate authentication from authorization: a known identity is not automatically allowed to perform every action.
- Enforce least privilege horizontally and vertically.
- Deny by default when no policy rule matches.
- Validate permission on every request, alternate route, background action, export, and static resource.
- Perform checks on the server side, close to the resource or state transition.
- Verify object-level and tenant-level checks for user-controlled IDs.
- Fail closed on missing policy data, exceptions, and middleware misconfiguration.

## Pattern Examples

### IDOR through user-controlled identifier

```ts
// Vulnerable
app.get("/accounts/:id", requireLogin, async (req, res) => {
  res.json(await accounts.get(req.params.id));
});
```

```ts
// Safer
app.get("/accounts/:id", requireLogin, async (req, res) => {
  const account = await accounts.get(req.params.id);
  if (!canReadAccount(req.user, account)) throw new Forbidden();
  res.json(account);
});
```

### Client-side admin control only

```js
// Vulnerable: hiding a button is not authorization.
if (!currentUser.isAdmin) hideDeleteButton();
```

```ts
// Safer: enforce on the server.
app.delete("/users/:id", requireLogin, requireRole("admin"), deleteUser);
```

### Fail-open policy handling

```python
# Vulnerable
try:
    allowed = policy_engine.check(user, action, resource)
except Exception:
    allowed = True
```

```python
try:
    allowed = policy_engine.check(user, action, resource)
except Exception:
    allowed = False
if not allowed:
    raise Forbidden()
```

## Review Prompts

- What is the subject, action, object, tenant, and environmental condition for this decision?
- Can a user change a resource ID and reach another tenant's data?
- Does an alternate export, batch, or async path repeat the same object-level check?
- Are static files and cloud objects protected by the same policy model?
- Do authorization failures leave partial state changes behind?

## Source

Local summary based on the OWASP Authorization Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html`
