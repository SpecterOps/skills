bremote_exec

Ask Beacon to run a command on a remote target.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the remote execute method to use

`$3` - the remote target

`$4` - the command and arguments to run

#### Example

```
# winrm [target] [command+args]
alias winrm-exec {
   bremote_exec($1, "winrm", $2, $3); {
}```

See also&beacon_remote_exec_method_describe, &beacon_remote_exec_method_register, &beacon_remote_exec_methods

