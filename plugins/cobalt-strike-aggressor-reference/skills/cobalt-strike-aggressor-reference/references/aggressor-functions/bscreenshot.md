bscreenshot

Ask Beacon to take a screenshot.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - (optional) the PID to inject the screenshot tool or $null

`$3` - (optional) the architecture of the target PID (x86|x64) or $null

#### Example

Spawn a temporary process```
item "&Screenshot" {
   binput($1, "screenshot");
   bscreenshot($1);
}```

Inject into the specified process```
bscreenshot($1, 1234, "x64");```

