powershell_command

Returns a one-liner to run a PowerShell expression (e.g., `powershell.exe -nop -w hidden -encodedcommand MgAgACsAIAAyAA==`)

#### Arguments

`$1` - the PowerShell expression to wrap into a one-liner.

`$2` - will the PowerShell command run on a remote target?

#### Returns

Returns a powershell.exe one-liner to run the specified expression.

#### Example

```
$cmd = powershell_command("2 + 2", false);
println($cmd);```

