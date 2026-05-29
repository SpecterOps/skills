openBrowserPivotSetup

open the browser pivot setup dialog

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Browser Pivoting" {
   local('$bid');
   foreach $bid ($1) {
      openBrowserPivotSetup($bid);
   }
}```
