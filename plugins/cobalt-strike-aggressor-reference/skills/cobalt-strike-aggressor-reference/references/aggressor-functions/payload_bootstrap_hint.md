payload_bootstrap_hint

Get the offset to function pointer hints used by Beacon's Reflective Loader. Populate these hints with the asked-for process addresses to have Beacon load itself into memory in a more OPSEC-safe way.

#### Arguments

`$1` - the payload position-independent code (specifically, Beacon)

`$2` - the function to get the patch location for

#### Notes

- Cobalt Strike's Beacon has a protocol to accept artifact-provided function pointers for functions required by Beacon's Reflective Loader. The protocol is to patch the location of **GetProcAddress** and **GetModuleHandleA** into the Beacon DLL. Use of this protocol allows Beacon to load itself in memory without triggering shellcode detection heuristics that monitor reads of kernel32's Export Address Table. This protocol is optional. Artifacts that don't follow this protocol will fallback to resolving key functions via the Export Address Table.
- The Artifact Kit and Resource Kit both implement this protocol. Download these kits to see how to use this function.

#### Returns

The offset to a memory location to patch with a pointer for a specific function used by Beacon's Reflective Loader.

