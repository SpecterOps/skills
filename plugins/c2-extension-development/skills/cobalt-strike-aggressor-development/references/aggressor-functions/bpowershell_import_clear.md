bpowershell_import_clear

Clear the imported PowerShell script from a Beacon session.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
alias powershell-clear {
   bpowershell_import_clear($1);
}```
