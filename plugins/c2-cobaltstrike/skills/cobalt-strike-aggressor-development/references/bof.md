# Aggressor Functions Used for BOF Loading and Interaction

You'll likely want to use Aggressor Script to run your finalized BOF implementations within Cobalt Strike. A BOF is a good place to implement a lateral movement technique, an escalation of privilege tool, or a new reconnaissance capability.

The &beacon_inline_execute function is Aggressor Script's entry point to run a BOF file. Here is a script to run a simple Hello World program:

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
}
```

The script first determines the architecture of the session. An x86 BOF will only run in an x86 Beacon session. Conversely, an x64 BOF will only run in an x64 Beacon session. This script then reads target BOF into an Aggressor Script variable. The next step is to pack our arguments. The &bof_pack function packs arguments in a way that is compatible with Beacon's internal data parser API. This script uses the customary &btask to log the action the user asked Beacon to perform. And, &beacon_inline_execute runs the BOF with its arguments.

The &beacon_inline_execute function accepts the Beacon ID as the first argument, a string containing the BOF content as a second argument, the entry point as its third argument, and the packed arguments as its fourth argument. The option to choose an entrypoint exists in case you choose to combine like-functionality into a single BOF.

Here is the C program that corresponds to the above script:

```
/*
 * Compile with:
 * x86_64-w64-mingw32-gcc -c hello.c -o hello.x64.o
 * i686-w64-mingw32-gcc -c hello.c -o hello.x86.o
 */

#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>
#include "beacon.h"

void demo(char * args, int length) {
	datap  parser;
	char * str_arg;
	int    num_arg;

	BeaconDataParse(&parser, args, length);
	str_arg = BeaconDataExtract(&parser, NULL);
	num_arg = BeaconDataInt(&parser);

	BeaconPrintf(CALLBACK_OUTPUT, "Message is %s with %d arg", str_arg, num_arg);
}
```

The demo function is our entrypoint. We declare the datap structure on the stack. This is an empty and uninitiated structure with state information for extracting arguments prepared with &bof_pack. BeaconDataParse initializes our parser. BeaconDataExtract extracts a length-prefixed binary blob from our arguments. Our pack function has options to pack binary blobs as zero-terminated strings encoded to the session's default character set, a zero-terminated wide-character string, or a binary blob without transformation. The BeaconDataInt extracts an integer that was packed into our arguments. BeaconPrintf is one way to format output and make it available to the operator.

## Functions

### bof_pack

Pack arguments in a way that's suitable for BOF APIs to unpack.

Arguments

$1 - the id for the Beacon (needed for unicode conversions)
$2 - format string for the packed data
... - one argument per item in our format string

Note

This function packs its arguments into a binary structure for use with `&beacon_inline_execute`. The format string options here correspond to the `BeaconData*` C API available to BOF files. This API handles transformations on the data and hints as required by each type it can pack.

The following are in the format:
Type - Description - Unpack With (C)

`b` - binary data -	`BeaconDataExtract`
`i` - 4-byte integer - `BeaconDataInt`
`s` - 2-byte short integer - `BeaconDataShort`
`z` - zero-terminated+encoded string - `BeaconDataExtract`
`Z` - zero-terminated wide-char string - `(wchar_t *)BeaconDataExtract`

### beacon_inline_execute

Execute a Beacon Object File

Arguments

$1 - the id for the Beacon
$2 - a string containing the BOF file
$3 - the entry point to call
$4 - packed arguments to pass to the BOF file
$5 - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

Example (hello.c)

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
}
```

Example (hello.cna)

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
}
```
