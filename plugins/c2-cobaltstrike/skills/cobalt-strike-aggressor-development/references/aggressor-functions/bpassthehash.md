bpassthehash

Ask Beacon to create a token that passes the specified hash. This is the pth command in Beacon. It uses mimikatz. This function requires administrator privileges.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the domain of the user

`$3` - the user's username

`$4` - the user's password hash

`$5 `- (optional) the PID to inject the pth command into or $null

`$6 `- (optional) the architecture of the target PID (x86|x64) or $null

#### Example

Spawn a temporary process```
bpassthehash($1, "CORP", "Administrator", "password_hash");```

Inject into the specified process```
bpassthehash($1, "CORP", "Administrator", "password_hash", 1234, "x64");```
