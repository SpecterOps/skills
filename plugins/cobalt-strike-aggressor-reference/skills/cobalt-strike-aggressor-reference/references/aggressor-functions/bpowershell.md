bpowershell

Ask Beacon to run a PowerShell cmdlet

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the cmdlet and arguments

`$3` - (optional) if specified, powershell-import script is ignored and this argument is treated as the download cradle to prepend to the command. Empty string is OK here too, for no download cradle. Specify $null to use the current imported PowerShell script.

`$4` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Example

```
# get the version of PowerShell...
alias powerver {
   bpowershell($1, '$PSVersionTable.PSVersion');
}```

