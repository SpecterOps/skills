bmimikatz

Ask Beacon to run a mimikatz command.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and arguments to run. Supports the semicolon ( **;** ) character to separate multiple commands

`$3` - (optional) the PID to inject the mimikatz command into or $null

`$4` - (optional) the architecture of the target PID (x86|x64) or $null

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Examples

```
# Usage: coffee [pid] [arch]
alias coffee {
   if ($2 >= 0 && ($3 eq "x86" || $3 eq "x64")) {
      bmimikatz($1, "standard::coffee", $2, $3);
   } else {
      bmimikatz($1, "standard::coffee");
   }
}```



```
alias double_espresso {
bmimikatz($1, "standard::coffee;standard::coffee");
}```

