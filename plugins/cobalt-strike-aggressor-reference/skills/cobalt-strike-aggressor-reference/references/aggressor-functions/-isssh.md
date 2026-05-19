-isssh

Check if a session is an SSH session or not.

#### Arguments

`$1` - Beacon/Session ID

#### Example

```
command ssh_sessions {
   foreach $session (beacons()) {
      if (-isssh $session['id']) {
         println($session);
      }
   }
}```

