btoken_store_use

Ask Beacon to use a token from the token store.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the token ID.

#### Example

```
alias token-store_use {
   btoken_store_use($1, int($2));
}```
