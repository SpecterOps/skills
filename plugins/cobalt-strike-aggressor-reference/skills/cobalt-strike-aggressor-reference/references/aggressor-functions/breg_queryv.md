breg_queryv

Ask Beacon to query a value within a registry key.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the path to the key

`$3` - the name of the value to query

`$4` - x86|x64 - which view of the registry to use

#### Example

```
alias winver {
   breg_queryv($1, "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion", "ProductName", "x86");
}```

