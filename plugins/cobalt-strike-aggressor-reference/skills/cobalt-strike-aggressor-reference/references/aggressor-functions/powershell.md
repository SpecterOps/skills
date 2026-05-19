powershell

DEPRECATED This function is deprecated in Cobalt Strike 4.0. Use &artifact_stager and &powershell_command instead.

Returns a PowerShell one-liner to bootstrap the specified listener.

#### Arguments

`$1` - the listener name

`$2` - [true/false]: is this listener targeting local host?

`$3` - x86|x64 - the architecture of the generated stager.

#### Notes

Be aware that not all listener configurations have x64 stagers. If in doubt, use x86.

#### Returns

A PowerShell one-liner to run the specified listener.

#### Example

```
println(powershell("my-listener", false));```

