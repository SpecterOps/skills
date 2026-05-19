bdrives

Ask Beacon to list the drives on the compromised system

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
item "&Drives" {
   binput($1, "drives");
   bdrives($1);
}```
