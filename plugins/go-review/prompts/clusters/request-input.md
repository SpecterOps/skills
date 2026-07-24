---
cluster_id: request-input
consolidated: true
---

# Request Input Review

Inventory body readers, JSON/YAML/XML decoders, multipart handlers, headers,
proxy metadata, path variables, and gRPC unmarshalling.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| BODY | unbounded-request-body | `io.ReadAll`, decoders, or multipart parsing without `MaxBytesReader`, size limits, or streaming bounds |
| DECODE | decoder-fail-open | parse errors ignored, partial objects accepted, duplicate-field ambiguity, or permissive decode fallback |
| HEADER | trusted-header-spoofing | `X-Forwarded-*`, `X-User-*`, internal headers, or metadata trusted without proxy/auth verification |

Focus on attacker-controlled request data crossing into auth, allocation, or storage decisions.
