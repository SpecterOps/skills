openElevateDialog

Open the dialog to launch a privilege escalation exploit.

#### Arguments

`$1` - the beacon ID

#### Example

```
item "Elevate" {
   local('$bid');
   foreach $bid ($1) {
      openElevateDialog($bid);
   }
}```

