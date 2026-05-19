bcheckin

Ask a Beacon to checkin. This is basically a no-op for Beacon.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
item "&Checkin" {
   binput($1, "checkin");
   bcheckin($1);
}```
