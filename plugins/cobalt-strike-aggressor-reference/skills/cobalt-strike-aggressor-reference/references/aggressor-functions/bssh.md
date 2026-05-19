bssh

Ask Beacon to spawn an SSH session.

#### Arguments

`$1` - id for the beacon. This may be an array or a single ID.

`$2` - IP address or hostname of the target

`$3` - port (e.g., 22)

`$4` - username

`$5` - password

`$6` - (optional) the PID to inject the SSH client into or $null

`$7` - (optional) the architecture of the target PID (x86|x64) or $null

#### Example

Spawn a temporary process```
bssh($1, "172.16.20.128", 22, "root", "toor");```

Inject into the specified process```
bssh($1, "172.16.20.128", 22, "root", "toor", 1234, "x64");```

