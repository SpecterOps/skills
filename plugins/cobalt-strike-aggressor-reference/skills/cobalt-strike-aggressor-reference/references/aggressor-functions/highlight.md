highlight

Insert an accent (color highlight) into Cobalt Strike's data model

#### Arguments

`$1` - the data model

`$2` - an array of rows to highlight

`$3` - the accent type

#### Notes

- Data model rows include: applications, beacons, credentials, listeners, services, and targets.
- Accent options are:

| Color |  |
| --- | --- |
| no highlight |  |
| Green |  |
| Red |  |
| Yellow |  |
| Grey |  |
| Dark Blue |  |

#### Example

```
command admincreds {
   local('@creds');
   
   # find all of our creds that are user Administrator.
   foreach $entry (credentials()) {
      if ($entry['user'] eq "Administrator") {
         push(@creds, $entry);
      }
   }
   
   # highlight all of them green!
   highlight("credentials", @creds, "good");
}```

