---
cluster_id: unsafe-cgo
consolidated: true
---

# Unsafe and cgo Review

Inventory `unsafe.Pointer`, `reflect.SliceHeader`, `uintptr`, `import "C"`,
foreign allocations, exported cgo functions, and length conversions.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| UNSAFEPTR | unsafe-pointer-lifetime | Go pointers outlive objects, cross GC boundaries, or are reconstructed unsafely |
| CGOOWN | cgo-ownership-confusion | mismatched allocator/free ownership or C memory exposed with wrong lifetime |
| LENCAST | length-truncation | attacker-controlled lengths truncate across C/Go integer widths or signedness |

File only when the unsafe edge is reachable from the service or an exposed library boundary.
