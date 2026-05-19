artifact_general

Generates a payload artifact from arbitrary shellcode.

#### Arguments

`$1` - the shellcode

`$2` - the artifact type

`$3` - x86|x64 - the architecture of the generated payload

| Description |  |
| --- | --- |
| a DLL |  |
| a plain executable |  |
| a powershell script |  |
| a python script |  |
| a service executable |  |

#### Note

While the Python artifact in Cobalt Strike is designed to simultaneously carry an x86 and x64 payload; this function will only populate the script with the architecture argument specified as `$3`

