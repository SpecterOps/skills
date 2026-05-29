---
name: c2-bof-development
description: Beacon Object File (BOF) development. Use when creating, porting, or debugging BOFs for C2 frameworks including API usage, DFR conventions, and compilation.
metadata:
  author: "GhostWorks"
---

# BOF Development Skill

## When to Use

Use this skill when developing BOF files (Beacon Object Files):
- Creating new BOFs from scratch
- Porting existing tools or repos into BOF format
- Looking up BOF API functions (BeaconPrintf, BeaconDataParse, etc.)
- Understanding Dynamic Function Resolution (DFR) conventions
- Compiling and building BOFs
- Linting BOF code with `boflint.py`

## When NOT to Use

Do not use this skill unless you are certain that you are creating a BOF file, or working on a BOF project.

## Terminology

- **BOF** - Beacon Object File - An object file format used by C2 frameworks for loading additional in-memory functionality
- **DFR** - Dynamic Function Resolution - A convention to declare and call Win32 APIs as `LIBRARY$Function`

## BOF Overview

BOFs are compiled C/C++ object files that execute in-memory within a C2 implant's process space. They provide a way to add functionality without writing artifacts to disk.

Example BOF that queries the primary Domain Controller:

```c
#include <windows.h>
#include <stdio.h>
#include <dsgetdc.h>
#include "beacon.h"

DECLSPEC_IMPORT DWORD WINAPI NETAPI32$DsGetDcNameA(LPVOID, LPVOID, LPVOID, LPVOID, ULONG, LPVOID);
DECLSPEC_IMPORT DWORD WINAPI NETAPI32$NetApiBufferFree(LPVOID);

void go(char * args, int alen) {
    PDOMAIN_CONTROLLER_INFO pdcInfo;
    DWORD dwRet = NETAPI32$DsGetDcNameA(NULL, NULL, NULL, NULL, 0, &pdcInfo);

    if (ERROR_SUCCESS == dwRet) {
        BeaconPrintf(CALLBACK_OUTPUT, "%s", pdcInfo->DomainName);
    }
    NETAPI32$NetApiBufferFree(pdcInfo);
}
```

## BOF Considerations

- **Minimal footprint** — reduce memory usage, only include what's needed
- **Stability** — a BOF crash kills the parent process; handle errors carefully
- **No disk artifacts** — avoid writing to disk; advise the user when unavoidable
- **Windows x64** — assume Windows x64 target unless told otherwise

## Linting

Use the included linter to check BOF code for common issues:

```bash
python3 ~/.agents/skills/bof/scripts/boflint.py <bof_source.c>
```

## References

* [DFR Information](./references/dynamic-function-resolution.md) - Dynamic Function Resolution process used in BOF development
* [API](./references/api.md) - BOF APIs for communication with C2 frameworks
* [Building](./references/building.md) - How to compile a BOF
