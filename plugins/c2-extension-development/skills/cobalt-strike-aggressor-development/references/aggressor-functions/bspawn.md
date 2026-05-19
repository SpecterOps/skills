bspawn

Ask Beacon to spawn a new session

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the listener to target.

`$3` - the architecture to spawn a process for (defaults to current beacon arch)

#### Example

```
item "&Spawn" {
   openPayloadHelper(lambda({
      binput($bids, "spawn x86 $1");
      bspawn($bids, $1, "x86");
   }, $bids => $1));
}```
