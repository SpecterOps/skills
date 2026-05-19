bsetenv

Ask Beacon to set an environment variable

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the environment variable to set

`$3` - the value to set the environment variable to (specify $null to unset the variable)

#### Example

```
alias tryit {
   bsetenv($1, "foo", "BAR!");
   bshell($1, "echo %foo%");
}```

