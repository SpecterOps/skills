---
cluster_id: crypto-session
consolidated: true
---

# Crypto, JWT, and Session Review

Inventory token generation, JWT parsing, TLS configs, cookies, password/session
handling, and secret comparisons.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| JWT | jwt-validation | algorithm confusion, missing audience/issuer/expiry checks, unsafe `ParseUnverified`, or key selection mistakes |
| RNG | weak-token-randomness | `math/rand`, predictable IDs, weak reset tokens, or reused nonces |
| TLS | tls-misconfiguration | `InsecureSkipVerify`, weak minimum versions, client cert mistakes, or unsafe defaults |
| COOKIE | cookie-session-flags | missing `Secure`, `HttpOnly`, `SameSite`, weak session rotation, or unsafe cookie scope |
| TIMING | timing-unsafe-compare | secrets, signatures, tokens, or MACs compared with ordinary string/byte equality |

Keep weak hardening separate from exploitable token forgery or auth bypass.
