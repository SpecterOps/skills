bprintscreen

Ask Beacon to take a screenshot via PrintScr method.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - (optional) the PID to inject the screenshot tool via PrintScr method or $null.

`$3` - (optional) the architecture of the target PID (x86|x64) or $null.

#### Example

Spawn a temporary process```
item "&Printscreen" {
   binput($1, "printscreen");
   bpintscreen($1);
}```

Inject into the specified process```
bprintscreen($1, 1234, "x64");```

