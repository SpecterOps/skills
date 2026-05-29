bargue_add

This function adds an option to Beacon's list of commands to spoof arguments for.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command to spoof arguments for. Environment variables are OK here too.

`$3` - the fake arguments to use when the specified command is run.

#### Notes

- The process match is exact. If Beacon tries to launch "net.exe", it will not match net, NET.EXE, or c:\windows\system32\net.exe. It will only match net.exe.
- x86 Beacon can only spoof arguments in x86 child processes. Likewise, x64 Beacon can only spoof arguments in x64 child processes.
- The real arguments are written to the memory space that holds the fake arguments. If the real arguments are longer than the fake arguments, the command launch will fail.

#### Example

```
# spoof cmd.exe arguments.
bargue_add($1, "%COMSPEC%", "/K \"cd c:\windows\temp & startupdatenow.bat\"");

# spoof net arguments
bargue_add($1, "net", "user guest /active:no");```
