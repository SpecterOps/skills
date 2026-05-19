brunu

Ask Beacon to run a process under another process.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the PID of the parent process

`$3` - the command + arguments to run

#### Example

```
brunu($1, 1234, "notepad.exe");```
