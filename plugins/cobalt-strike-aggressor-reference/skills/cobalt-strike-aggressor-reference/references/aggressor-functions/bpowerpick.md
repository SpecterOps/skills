bpowerpick

Spawn a process, inject Unmanaged PowerShell, and run the specified command.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the cmdlet and arguments

`$3` - (optional) if specified, powershell-import script is ignored and this argument is treated as the download cradle to prepend to the command. Empty string is OK here too, for no download cradle. Specify $null to use the current imported PowerShell script.

`$4` - (optional) the "PATCHES:" argument can modify functions in memory for the process. Up to 4 "patch-rule" rules can be specified (space delimited).

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

**"patch-rule" syntax (comma delimited):**` [library],[function],[offset],[hex-patch-value]`

**library **- 1-260 characters
**function **- 1-256 characters
**offset **- 0-65535 (The offset from the start of the executable function)
**hex-patch-value** - 2-200 hex characters (0-9,A-F). Length must be even number (hex pairs).

#### Example

```
# get the version of PowerShell available via Unmanaged PowerShell
alias powerver {
   bpowerpick($1, '$PSVersionTable.PSVersion');
}
  
alias powerver2 {
   bpowerpick($1, '$PSVersionTable.PSVersion', '', 'PATCHES: ntdll.dll,EtwEventWrite,0,C300');
}```

