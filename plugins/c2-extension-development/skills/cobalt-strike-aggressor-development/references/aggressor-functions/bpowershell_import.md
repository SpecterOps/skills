bpowershell_import

Import a PowerShell script into a Beacon

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the path to the local file to import

#### Example

```
# quickly run PowerUp
alias powerup {
   bpowershell_import($1, script_resource("PowerUp.ps1"));
   bpowershell($1, "Invoke-AllChecks");
}```
