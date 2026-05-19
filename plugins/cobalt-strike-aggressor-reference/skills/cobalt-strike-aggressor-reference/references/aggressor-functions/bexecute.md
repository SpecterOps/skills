bexecute

Ask Beacon to execute a command [without a shell]. This provides no output to the user.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and arguments to run

#### Example

```
bexecute($1, "notepad.exe");```

