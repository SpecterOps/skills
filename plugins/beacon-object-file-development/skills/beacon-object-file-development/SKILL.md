---
name: beacon-object-file-development
description: Provides information on how to develop BOF files (Beacon Object Files), including API information and useful steps
license: MIT
metadata:
  author: xpn
  version: "0.1.0"
  category: security
---

# BOF Development Skill

## When to Use

Use this skill when developing BOF files (Beacon Object Files). This skill will provide you with all the information that you need to be an expert in BOF development.

Typical requests for BOF project assistance would be:

- "Take this repository and port this into a BOF"
- "Take this idea and create a BOF"

## When NOT to Use

Do not use this skill unless you are certain that you are creating a BOF file, or working on a BOF project. Often you will be told that this is the case.

## Terminology

- BOF - Beacon Object File - An object file format used by C2 frameworks for loading additional in-memory functionality
- DFR - Dynamic Function Resolution - Dynamic Function Resolution is a convention to declare and call Win32 APIs as `LIBRARY$Function`

## BOF Overview

BOFs are traditionally written in C. For example, the following BOF queries the name of the primary Domain Controller in an Active Directory domain:

```
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

A BOF is used when we want to add functionality to a C2 framework which executes purely in memory. When completing security assessments, one common detection mechanism used by endpoint security products is to review files written to disk. Due to this, the BOF specificaiton was created with the purpose of:

1. Defining a standard that would allow BOFs to be used agnostic of the C2 framework
2. Define API's that can be used to support in-memory execution

Due to this, you should always consider if functionality being added to a BOF upon development would involve artifacts being written to disk. Sometimes this is unavoidable, but you should make every attempt to avoid this, and advise the user that this is the case.

## BOF Code

When writing C or C++ code which will be compiled into a BOF, the following should always be considered:

- Minimal code to do the job - A BOF is executed in-memory, so we want to reduce the memory footprint as much as we can. The code generated should be the minimum required to do the job well, and do the job safely
- Stability - A BOF executes within a C2 implants memory address space. This means that if the BOF crashes, so does the parent process. All attempts should be made to avoid scenarios where a crash may occur.
- Windows target - BOFs are developed for the Windows operating system (x64 Windows). Unless you are explicitly told otherwise, always assume that the target execution environment will be a Windows x64 system.

## BOF Code Porting

An important task that you may be asked to complete is that of taking an existing codebase and creating a BOF port.

When being asked to do this, you should consider:

 - The code being ported should be the source of truth. Do not attempt to identify issues in the source codebase unless this will cause a specific issue when porting. In this case you should call out the issue to the user and what your proposed fix would be.
 - Remember that BOFs are often used on offensive security assessments. This means that the code you are working with may appear to produce outputs which may be unusual. If you encounter this you should:
   - Verify with the original research (if available) that the output is actually intended as part of the research
   - Only call out and modify the implementation if it is an obvious issue to the stability of the BOF
   - Explicitly call out any purposefully obfuscated intentions behind the source code not intended to be part of the research or which may cause damage

## References

For more detailed information on a specific area of BOF development, we have the following references:

* [DFR Information](./references/dynamic-function-resolution.md) - Provides information on the DFR process used in BOF development
* [API](./references/api.md) - Provides information on the API's supported by BOFs for communication with a C2 framework
* [Building](./references/building.md) - Provides information on how to compile a BOF
