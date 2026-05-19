openPortScannerLocal

Open the port scanner dialog with options to target a Beacon's local network

#### Arguments

`$1` - the beacon to target with this feature

#### Example

```
item "Scan" {
   local('$bid');
   foreach $bid ($1) {
      openPortScannerLocal($bid);
   }
}```

