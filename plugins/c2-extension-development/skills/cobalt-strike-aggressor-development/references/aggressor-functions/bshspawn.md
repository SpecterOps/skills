bshspawn

Spawn shellcode (from a local file) into another process. This function benefits from Beacon's configuration to spawn post-exploitation jobs (e.g., spawnto, ppid, etc.)

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the process architecture (x86 | x64)

`$3` - the local file with the shellcode

#### Example

```
bshspawn($1, "x86", "/path/to/stuff.bin");```
