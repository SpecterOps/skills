blink

Ask Beacon to link to a host over a named pipe

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target to link to

`$3` - (optional) the pipename to use. The default pipename in the Malleable C2 profile is the default otherwise.

#### Note

Use &beacon_link if you want a script function that will connect or link based on a listener configuration.

#### Example

```
blink($1, "DC");```

