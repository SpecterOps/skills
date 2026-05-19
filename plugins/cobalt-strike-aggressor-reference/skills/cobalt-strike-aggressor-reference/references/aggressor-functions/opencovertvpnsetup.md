openCovertVPNSetup

open the Covert VPN setup dialog

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "VPN Pivoting" {
   local('$bid');
   foreach $bid ($1) {
      openCovertVPNSetup($bid);
   }
}```

