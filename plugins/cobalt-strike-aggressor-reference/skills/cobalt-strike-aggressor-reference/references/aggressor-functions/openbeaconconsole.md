openBeaconConsole

Open the console to interact with a Beacon

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Interact" {
   local('$bid');
   foreach $bid ($1) {
      openBeaconConsole($bid);
   }
}```

