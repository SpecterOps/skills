bgetsystem

Ask Beacon to attempt to get the SYSTEM token.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
item "Get &SYSTEM" {
   binput($1, "getsystem");
   bgetsystem($1);
}```
