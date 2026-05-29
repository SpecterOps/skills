artifact_payload

Generates a stageless payload artifact (exe, dll) from a Cobalt Strike listener name

#### Arguments

`$1` - the listener name

`$2` - the artifact type

`$3` - x86|x64 - the architecture of the generated payload (stage)

`$4` - exit method: 'thread' (leave the thread when done) or 'process' (exit the process when done). Use 'thread' if injecting into an existing process.

`$5` – A string value for the system call method. Valid values are:

**None**: Use the standard Windows API function.**Direct**: Use the Nt* version of the function.

**Indirect**: Jump to the appropriate instruction within the Nt* version of the function.

| Description |  |
| --- | --- |
| a DLL |  |
| a plain executable |  |
| a powershell script |  |
| a python script |  |
| raw payload stage |  |
| a service executable |  |

`$6` - (optional) The supporting HTTP library for generated beacons (wininet|winhttp|$null|blank string).

`$7` - (optional) DNS Comm Mode Override. Use this to change the DNS Comm Mode from the default mode defined in Malleable C2 (dns|dns_over_https|$null|blank string).

#### Note

While the Python artifact in Cobalt Strike is designed to simultaneously carry an x86 and x64 payload; this function will only populate the script with the architecture argument specified as `$3`

#### Example

```
$data = artifact_payload("my-listener", "exe", "x86", “process”, “Indirect”);```
