beacons

Get information about all Beacons calling back to this Cobalt Strike team server.

#### Returns

An array of dictionary objects with information about each beacon.

#### Example

```
foreach $beacon (beacons()) {
   println("Bid: " . $beacon['id'] . " is " . $beacon['name']);
}```

