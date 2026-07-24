# OWASP NoSQL Security

Use this reference when reviewing MongoDB, CouchDB, Cassandra, DynamoDB, Elasticsearch-like query DSLs, ODMs, or any structured query object built from attacker input.

## Review Checks

- Reject raw client-supplied query fragments, operators, aggregation stages, and executable expressions.
- Validate types and allowlisted fields before constructing filters or sort clauses.
- Review driver and ODM escape hatches, `eval`-like features, and server-side scripting.
- Check authentication, TLS, network exposure, admin interfaces, secrets, backups, and least-privilege database roles.
- Look for operator injection through JSON objects even when no strings are concatenated.

## Pattern Examples

### Raw filter passthrough

```js
// Vulnerable: attacker can submit operators such as {"$ne": null}.
const user = await users.findOne(req.body.filter);
```

```js
// Safer
const email = String(req.body.email);
const user = await users.findOne({ email });
```

### Executable query fragment

```js
// Vulnerable
const filter = eval("(" + req.query.filter + ")");
db.collection("users").find(filter);
```

```js
// Safer
const allowedFields = new Set(["email", "status"]);
const field = String(req.query.field);
if (!allowedFields.has(field)) throw new BadRequest("invalid field");
db.collection("users").find({ [field]: String(req.query.value) });
```

### Unbounded operator support

```ts
// Vulnerable
const query = { ...req.body };
await collection.find(query).toArray();
```

```ts
// Safer
const query = {
  status: validateEnum(req.body.status, ["active", "disabled"]),
  tenantId: authenticatedTenantId
};
await collection.find(query).toArray();
```

## Review Prompts

- Can the client inject `$where`, `$regex`, `$expr`, or equivalent operators?
- Does the query layer accept raw JSON or DSL fragments?
- Is the database reachable from the public network or running with default/open access?
- Are service accounts separated for read, write, admin, and backup operations?

## Source

Local summary based on the OWASP NoSQL Security Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html`
