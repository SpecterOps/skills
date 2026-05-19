bread_pipe

bread_pipe is called to register a new user-defined post-ex Beacon job which communicates over a named pipe.

#### Arguments

$1 - the Beacon id

$2 - the job type (ANONYMOUS_BYTESTREAM, ANONYMOUS_BLOB, or IMPERSONATE_BYTESTREAM)

$3 - the callback type (CALLBACK_POSTEX_KIT, CALLBACK_OUTPUT, CALLBACK_OUTPUT_UTF8, or CALLBACK_OUTPUT_OEM).

NOTE: The CALLBACK_POSTEX_KIT type is not supported when using ANONYMOUS_BLOB as the job type.$4 - the job description

$5 - the name of the named pipe Beacon must connect to for communication

$6 - the pid (set to 0)

$7 - the timeout value in milliseconds

$8 - an optional aggressor script closure (can be set to $null)

#### Example

```
bread_pipe($bid, "ANONYMOUS_BYTESTREAM", "CALLBACK_POSTEX_KIT", "bof.x64.o", "msrpc_1234", 0, 10000, $null);```
