btoken_store_steal_and_use

Ask Beacon to steal a token, store it and immediately apply it to the beacon.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the PID to take the token from.

`$3` - the OpenProcessToken access mask.

#### Example

```
alias token-store_steal_and_use {
   btoken_store_steal_and_use($1, int($2), 11);
}```
