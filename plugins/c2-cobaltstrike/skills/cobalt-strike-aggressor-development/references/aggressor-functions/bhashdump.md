bhashdump

Ask Beacon to dump local account password hashes. If injecting into a pid that process requires administrator privileges.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2 `- the PID to inject the hashdump dll into or $null.

`$3 `- (optional) the architecture of the target PID (x86|x64) or $null.

`$4` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map.

#### Example

Spawn a temporary process```
item "Dump &Hashes" {
   binput($1, "hashdump");
   bhashdump($1);
}```

Inject into the specified process)```
bhashdump($1, 1234, "x64");```
