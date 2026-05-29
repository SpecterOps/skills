brev2self

Ask Beacon to drop its current token. This calls the RevertToSelf() Win32 API.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
alias rev2self {
   brev2self($1);
}```
