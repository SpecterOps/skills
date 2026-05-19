# Query Snapshot Safety Scan

Static review helper for vendored query snapshots. This is intentionally conservative and does not replace manual review before running a query against a real BloodHound instance.

- Potential write-clause hits: `0`
- Broad node matches without LIMIT: `3`

## Broad node matches without LIMIT

| Query | Snapshot |
| --- | --- |
| Accounts related to AAD Entra Connect | `references/query-snapshots/bloodhound-query-library/queries/Accounts related to AAD Entra Connect.yml` |
| Non-Tier Zero account with 'Admin Count' flag | `references/query-snapshots/bloodhound-query-library/queries/Non-Tier Zero account with 'Admin Count' flag.yml` |
| Tier Zero users with email | `references/query-snapshots/bloodhound-query-library/queries/Tier Zero users with email.yml` |
