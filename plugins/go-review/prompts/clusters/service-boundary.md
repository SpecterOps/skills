---
cluster_id: service-boundary
consolidated: true
---

# Service Boundary Review

Build an inventory of routes, gRPC methods, middleware/interceptors, service
methods, repository calls, and actor/tenant identifiers.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| AUTHZ | missing-route-authorization | route or RPC method reaches privileged logic without an authorization check |
| TENANT | tenant-isolation-bypass | attacker-controlled object IDs or tenant IDs reach storage without ownership scoping |
| DEPUTY | confused-deputy | service credentials or privileged backend calls are reused on behalf of an untrusted caller |

Do not assume middleware coverage from naming alone; trace each entry point.
