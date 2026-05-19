-isactive

Check if a session is active or not. A session is considered active if (a) it has not acknowledged an exit message AND (b) it is not disconnected from a parent Beacon. 

#### Arguments

`$1` - Beacon/Session ID

#### Example

```
command active {
   local('$bid');
   foreach $bid (beacon_ids()) {
      if (-isactive $bid) {
         println("$bid is active!");
      }
   }
}```

