bblockdlls

Launch child processes with binary signature policy that blocks non-Microsoft DLLs from loading in the process space.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - true or false; block non-Microsoft DLLs in child process

#### Note

This attribute is available in Windows 10 only.

#### Example

```
on beacon_initial {
   binput($1, "blockdlls start");
   bblockdlls($1, true);
}```
