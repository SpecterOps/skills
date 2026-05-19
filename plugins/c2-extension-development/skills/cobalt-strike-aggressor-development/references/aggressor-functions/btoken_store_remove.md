btoken_store_remove

Ask Beacon to remove specific access tokens from the store.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the array of token IDs to remove.

#### Example

```
alias token-store_remove {
   btoken_store_remove($1, @(int($2)));
}```
