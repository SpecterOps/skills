beacon_inline_execute

Execute a Beacon Object File

#### Arguments

`$1` - the id for the Beacon

`$2` - a string containing the BOF file

`$3` - the entry point to call

`$4` - packed arguments to pass to the BOF file

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Note

The Cobalt Strike documentation has a page specific to BOF files. See *Beacon Object Files*.

#### Example (hello.c)

```
/*
* Compile with:
* x86_64-w64-mingw32-gcc -c hello.c -o hello.x64.o
* i686-w64-mingw32-gcc -c hello.c -o hello.x86.o
*/

#include "windows.h"
#include "stdio.h"
#include "tlhelp32.h"
#include "beacon.h"

void demo(char * args, int length) {
   datap  parser;
   char * str_arg;
   int    num_arg;
   
   BeaconDataParse(&parser, args, length);
   str_arg = BeaconDataExtract(&parser, NULL);
   num_arg = BeaconDataInt(&parser);
   
   BeaconPrintf(CALLBACK_OUTPUT, "Message is %s with %d arg", str_arg, num_arg);
}```

#### Example (hello.cna)

```
alias hello {
   local('$barch $handle $data $args');

   # figure out the arch of this session
   $barch  = barch($1);

   # read in the right BOF file
   $handle = openf(script_resource("hello. $+ $barch $+ .o"));
   $data   = readb($handle, -1);
   closef($handle);

   # pack our arguments
   $args   = bof_pack($1, "zi", "Hello World", 1234);

   # announce what we're doing
   btask($1, "Running Hello BOF");
   
   # execute it.
   beacon_inline_execute($1, $data, "demo", $args);
}```

See Also&bof_pack

