---
cluster_id: sql-storage
consolidated: true
---

# SQL and Storage Review

Inventory SQL drivers, ORM calls, query construction, transaction boundaries,
tenant filters, scan errors, and storage abstraction wrappers.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| SQLI | sql-injection | string-built SQL, unsafe `fmt.Sprintf`, raw clauses, or interpolated identifiers |
| SQLTENANT | tenant-filter-omission | object fetch/update/delete without tenant or owner scoping |
| TXBOUND | transaction-boundary | authorization, balance, quota, or state changes split across unsafe transaction boundaries |
| QUERYERR | ignored-query-error | ignored `Scan`, `Rows.Err`, `Commit`, or query errors that fail open |

Do not confuse parameterized queries with safe authorization logic.
