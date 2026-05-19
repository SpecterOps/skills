bmode

Change the data channel for a DNS Beacon.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the data channel (e.g., dns, dns6, or dns-txt)

#### Example

```
item "Mode DNS-TXT" {
   binput($1, "mode dns-txt");
   bmode($1, "dns-txt");
}```
