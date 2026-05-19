openOrActivate

If a Beacon console exists, make it active. If a Beacon console does not exist, open it.

#### Arguments

`$1` - the Beacon ID

#### Example

```
item "&Activate" {
   local('$bid');
   foreach $bid ($1) {
      openOrActivate($bid);
   }
}```
