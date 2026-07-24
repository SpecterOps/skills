# OWASP SQL Injection Prevention

Use this reference when untrusted input reaches SQL, HQL, stored procedures, query builders, or raw ORM escape hatches.

## Review Checks

- Search for string concatenation, interpolation, template literals, and format strings in query text.
- Review dynamic `WHERE`, `ORDER BY`, `LIMIT`, table, and column fragments separately from data values.
- Verify stored procedures do not construct raw SQL internally.
- Treat escaping as a fallback layer, not the primary defense.
- Check database privileges and views so an injection cannot exceed the application's minimum needs.

## Pattern Examples

### String-built query

```ts
// Vulnerable
const sql = "SELECT * FROM users WHERE email = '" + req.query.email + "'";
const user = await db.query(sql);
```

```ts
// Safer
const user = await db.query(
  "SELECT * FROM users WHERE email = ?",
  [req.query.email]
);
```

### Dynamic sort direction

```python
# Vulnerable: identifiers usually cannot be parameter-bound.
sql = f"SELECT * FROM orders ORDER BY created_at {request.args['direction']}"
```

```python
direction = request.args.get("direction", "desc").lower()
if direction not in {"asc", "desc"}:
    raise BadRequest("invalid direction")
sql = f"SELECT * FROM orders ORDER BY created_at {direction}"
```

### Raw ORM escape hatch

```java
// Vulnerable
session.createQuery("from Inventory where productID='" + productId + "'");

// Safer
Query<Inventory> q = session.createQuery(
    "from Inventory where productID=:productId",
    Inventory.class
);
q.setParameter("productId", productId);
```

## Review Prompts

- Which values are data parameters, and which are query structure?
- Is an allowlist used for unavoidable dynamic identifiers?
- Does the application account have broader DB privileges than the path needs?
- Can an error path leak SQL details or change authorization behavior?

## Source

Local summary based on the OWASP SQL Injection Prevention Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html`
