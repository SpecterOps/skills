artifact_stager

Generates a stager artifact (exe, dll) from a Cobalt Strike listener

#### Arguments

`$1` - the listener name

`$2` - the artifact type

`$3` - x86|x64 - the architecture of the generated stager

| Description |  |
| --- | --- |
| a DLL |  |
| a plain executable |  |
| a powershell script |  |
| a python script |  |
| the raw file |  |
| a service executable |  |
| a Visual Basic script |  |

#### Note

Be aware that not all listener configurations have x64 stagers. If in doubt, use x86.

#### Returns

A scalar containing the specified artifact.

#### Example

```
$data = artifact_stager("my-listener", "exe", "x86");
 
$handle = openf(">out.exe");
writeb($handle, $data);
closef($handle);```

