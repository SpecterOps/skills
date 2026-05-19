# Dynamic Function Resolution

GetProcAddress, LoadLibraryA, GetModuleHandle, and FreeLibrary are available within BOF files. You have the option to use these to resolve Win32 APIs you wish to call. Another option is to use Dynamic Function Resolution (DFR).

Dynamic Function Resolution is a convention to declare and call Win32 APIs as LIBRARY$Function. This convention provides Beacon with the information it needs to explicitly resolve the specific function and make it available to your BOF file before it runs. When this process fails, Cobalt Strike will refuse to execute the BOF and tell you which function it couldn't resolve. Beacon supports 128 functions defined as a Dynamic Function.

Here's an example BOF that uses DFR and looks up the current domain:

```
#include <windows.h>
#include <stdio.h>
#include <dsgetdc.h>
#include "beacon.h"

DECLSPEC_IMPORT DWORD WINAPI NETAPI32$DsGetDcNameA(LPVOID, LPVOID, LPVOID, LPVOID,
                                                   ULONG, LPVOID);
DECLSPEC_IMPORT DWORD WINAPI NETAPI32$NetApiBufferFree(LPVOID);

void go(char * args, int alen) {
	DWORD dwRet;
	PDOMAIN_CONTROLLER_INFO pdcInfo;

	dwRet = NETAPI32$DsGetDcNameA(NULL, NULL, NULL, NULL, 0, &pdcInfo);
	if (ERROR_SUCCESS == dwRet) {
		BeaconPrintf(CALLBACK_OUTPUT, "%s", pdcInfo->DomainName);
	}

	NETAPI32$NetApiBufferFree(pdcInfo);
}
```

The above code makes DFR calls to DsGetDcNameA and NetApiBufferFree from NETAPI32. When you declare function prototypes for Dynamic Function Resolution, pay close attention to the decorators attached to the function declaration. Keywords, such as WINAPI and DECLSPEC_IMPORT are important. These decorations provide the compiler with the needed hints to pass arguments and generate the right call instruction.
