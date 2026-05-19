btoken_store_steal

Ask Beacon to steal a token and store it in the token store.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the array of PIDs to take the tokens from.

`$3` - the OpenProcessToken access mask.

#### Example

```
alias token-store_steal {
   btoken_store_steal($1, @(int($2)), 11);
}```

