bjump

Ask Beacon to spawn a session on a remote target.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the technique to use

`$3` - the remote target

`$4` - the listener to spawn

#### Example

```
# winrm [target] [listener]
alias winrm {
   bjump($1, "winrm", $2, $3);
}```

See also&beacon_remote_exploit_describe, &beacon_remote_exploit_register, &beacon_remote_exploits

