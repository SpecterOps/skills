beacon_link

This function links to an SMB or TCP listener. If the specified listener is not an SMB or TCP listener, this function does nothing.

#### Arguments

`$1` - the id of the beacon to link through

`$2` - the target host to link to. Use $null for localhost.

`$3` - the listener to link

#### Example

```
# smartlink [target] [listener name]
alias smartlink {
   beacon_link($1, $2, $3);
}```
