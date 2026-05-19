brportfwd

Ask Beacon to setup a reverse port forward.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the port to bind to on the target

`$3` - the host to forward connections to

`$4` - the port to forward connections to

#### Example

```
brportfwd($1, 80, "192.168.12.88", 80);```

