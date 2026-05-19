bscreenwatch

Ask Beacon to take periodic screenshots

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - (optional) the PID to inject the screenshot tool or $null

`$3` - (optional) the architecture of the target PID (x86|x64) or $null

#### Example

Spawn a temporary process```
item "&Screenwatch" {
   binput($1, "screenwatch");
   bscreenwatch($1);
}```

Inject into the specified process```
bscreenwatch($1, 1234, "x64");```

