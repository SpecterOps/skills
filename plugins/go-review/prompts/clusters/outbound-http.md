---
cluster_id: outbound-http
consolidated: true
---

# Outbound HTTP Review

Inventory every outbound URL construction, redirect behavior, client transport,
header forwarding, metadata access, and timeout configuration.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| SSRF | ssrf | attacker-influenced URL, host, scheme, or redirect reaches outbound requests without destination controls |
| REDIRECT | redirect-credential-leak | auth headers, cookies, or internal credentials follow redirects or cross hosts |
| HTTPTIME | missing-http-timeout | client, transport, or request context lacks bounded timeouts on attacker-influenced paths |

Prove the attacker controls the destination or response behavior before filing.
