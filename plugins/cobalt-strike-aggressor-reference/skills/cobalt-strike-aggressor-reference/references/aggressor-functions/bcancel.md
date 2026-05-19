bcancel

Cancel a file download

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the file to cancel or a wildcard.

#### Example

```
item "&Cancel Downloads" {
   bcancel($1, "*");
}```

