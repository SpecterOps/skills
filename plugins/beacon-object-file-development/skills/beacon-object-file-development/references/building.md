# How do I develop a BOF?

Here's a Hello World BOF:

```
#include <windows.h>
#include "beacon.h"

void go(char * args, int alen) {
	BeaconPrintf(CALLBACK_OUTPUT, "Hello World: %s", args);
}
```

To compile this with Visual Studio (when being built on a Windows system):

```
cl.exe /c /GS- hello.c /Fohello.o
```

To compile this with x86 MinGW (when being built on a *nix system):

```
i686-w64-mingw32-gcc -c hello.c -o hello.o
```

To compile this with x64 MinGW (when being built on a *nix system):

```
x86_64-w64-mingw32-gcc -c hello.c -o hello.o
```

To lint a compiled BOF file, the `boflint.py` tool can be used as:

```
python boflint.py --loader any coff_compiled_file
```

beacon.h contains definitions for several internal Beacon APIs. The function go is similar to main in any other C program. It's the function that's called by inline-execute and arguments are passed to it. BeaconOutput is an internal Beacon API to send output to the operator. Not much to it.