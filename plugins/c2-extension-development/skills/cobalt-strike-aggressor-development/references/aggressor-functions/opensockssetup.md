openSOCKSSetup

open the SOCKS proxy server setup dialog

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "SOCKS Server" {
   local('$bid');
   foreach $bid ($1) {
      openSOCKSSetup($bid);
   }
}```
