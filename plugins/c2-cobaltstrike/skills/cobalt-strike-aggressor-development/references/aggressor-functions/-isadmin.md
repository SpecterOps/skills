-isadmin

Check if a session has admin rights

#### Arguments

`$1` - Beacon/Session ID

#### Example

```
command admin_sessions {
   foreach $session (beacons()) {
      if (-isadmin $session['id']) {
         println($session);
      }
   }
}```
