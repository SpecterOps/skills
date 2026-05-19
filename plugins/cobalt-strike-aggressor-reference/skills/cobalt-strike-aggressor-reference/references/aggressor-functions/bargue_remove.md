bargue_remove

This function removes an option to Beacon's list of commands to spoof arguments for.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command to spoof arguments for. Environment variables are OK here too.

#### Example

```
# don't spoof cmd.exe
bargue_remove($1, "%COMSPEC%");```

