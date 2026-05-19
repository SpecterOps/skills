artifact

DEPRECATED This function is deprecated in Cobalt Strike 4.0. Use &artifact_stager instead.

Generates a stager artifact (exe, dll) from a Cobalt Strike listener

#### Arguments

`$1` - the listener name

`$2` - the artifact type

`$3` - deprecated; this parameter no longer has any meaning.

`$4` - x86|x64 - the architecture of the generated stager

| Description |  |
| --- | --- |
| an x86 DLL |  |
| an x64 DLL |  |
| a plain executable |  |
| a powershell script |  |
| a python script |  |
| a service executable |  |
| a Visual Basic script |  |

#### Note

Be aware that not all listener configurations have x64 stagers. If in doubt, use x86.

#### Returns

A scalar containing the specified artifact.

#### Example

```
$data = artifact("my-listener", "exe");

$handle = openf(">out.exe");
writeb($handle, $data);
closef($handle);```

