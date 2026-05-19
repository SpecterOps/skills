belevate

Ask Beacon to spawn an elevated session with a registered technique.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the exploit to fire

`$3` - the listener to target.

#### Example

```
item "&Elevate 31337" {
   openPayloadHelper(lambda({
      binput($bids, "elevate ms14-058 $1");
      belevate($bids, "ms14-058", $1);
   }, $bids => $1));
}```

See also&beacon_exploit_describe, &beacon_exploit_register, &beacon_exploits

