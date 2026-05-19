bconnect

Ask Beacon (or SSH session) to connect to a Beacon peer over a TCP socket

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target to connect to

`$3` - (optional) the port to use. Default profile port is used otherwise.

#### Note

Use &beacon_link if you want a script function that will connect or link based on a listener configuration.

#### Example

```
bconnect($1, "DC");```
