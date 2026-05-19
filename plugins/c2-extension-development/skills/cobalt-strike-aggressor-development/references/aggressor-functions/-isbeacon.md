-isbeacon

Check if a session is a Beacon or not.

#### Arguments

`$1` - Beacon/Session ID

#### Example

```
command beacons {
   foreach $session (beacons()) {
      if (-isbeacon $session['id']) {
         println($session);
      }
   }
}```
