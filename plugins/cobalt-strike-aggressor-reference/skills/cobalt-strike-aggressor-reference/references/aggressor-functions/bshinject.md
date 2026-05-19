bshinject

Inject shellcode (from a local file) into a specific process.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the PID of the process to inject into

`$3` - the process architecture (x86 | x64)

`$4` - the local file with the shellcode

#### Example

```
bshinject($1, 1234, "x86", "/path/to/stuff.bin");```

