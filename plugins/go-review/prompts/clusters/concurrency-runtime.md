---
cluster_id: concurrency-runtime
consolidated: true
---

# Concurrency and Runtime Review

Inventory goroutines, channels, shared maps, sync primitives, contexts, timers,
request-scoped caches, and background work.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| MAPRACE | shared-map-race | unsynchronized maps or shared state reachable from concurrent handlers |
| GOROUTINE | goroutine-leak | goroutines, timers, or channels that outlive canceled requests or attacker-controlled work |
| CTX | missing-context-cancellation | outbound calls, DB queries, or background work drop request context or ignore cancellation |
| AUTHRACE | auth-cache-race | authz/session/cache state races that produce stale or cross-user authorization decisions |

Do not file generic race speculation; tie the race to a security invariant or reliable DoS path.
