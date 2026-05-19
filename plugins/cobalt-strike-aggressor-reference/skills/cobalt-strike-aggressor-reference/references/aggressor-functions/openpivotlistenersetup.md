openPivotListenerSetup

open the pivot listener setup dialog

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Listener..." {
   local('$bid');
   foreach $bid ($1) {
      openPivotListenerSetup($bid);
   }
}```

