openMakeTokenDialog

Open a dialog to help generate an access token.

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Make Token" {
   local('$bid');
   foreach $bid ($1) {
      openMakeTokenDialog($bid);
   }
}```
