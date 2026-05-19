openSpawnAsDialog

Open dialog to spawn a payload as another user

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Spawn As..." {
   local('$bid');
   foreach $bid ($1) {
      openSpawnAsDialog($bid);
   }
}```
