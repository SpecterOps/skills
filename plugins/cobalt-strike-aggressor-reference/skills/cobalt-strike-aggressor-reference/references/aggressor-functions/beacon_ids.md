beacon_ids

Get the ID of all Beacons calling back to this Cobalt Strike team server.

#### Returns

An array of beacon IDs

#### Example

```
foreach $bid (beacon_ids()) {
   println("Bid: $bid");
}```

