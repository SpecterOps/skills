bpsinject

Inject Unmanaged PowerShell into a specific process and run the specified cmdlet. This will use the current imported powershell script.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the process to inject the session into

`$3` - the process architecture (x86 | x64)

`$4` - the cmdlet to run

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Example

```
bpsinject($1, 1234, x64, "[System.Diagnostics.Process]::GetCurrentProcess()");```
