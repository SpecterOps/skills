brun

Ask Beacon to run a command

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and arguments to run

#### Note

This capability is a simpler version of the &beacon_execute_job function. The latter function is what &bpowershell and &bshell build on. This is a (slightly) more OPSEC-safe option to run commands and receive output from them.

#### Example

```
alias w {
   brun($1, "whoami /all");
}```
