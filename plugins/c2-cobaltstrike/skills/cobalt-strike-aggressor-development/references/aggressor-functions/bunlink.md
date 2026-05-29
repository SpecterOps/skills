bunlink

Ask Beacon to delink a Beacon its connected to over a TCP socket or named pipe.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target host to unlink (specified as an IP address)

`$3` - (optional) the PID of the target session to unlink

#### Example

```
bunlink($1, "172.16.48.3");```
