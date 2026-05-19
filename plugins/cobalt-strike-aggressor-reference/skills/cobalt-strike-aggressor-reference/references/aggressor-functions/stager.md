stager

Returns the stager for a specific Cobalt Strike listener 

#### Arguments

`$1` - the listener name

`$2` - x86|x64 - the architecture of the stager output. 

#### Note

Be aware that not all listener configurations have x64 stagers. If in doubt, use x86.

#### Returns

A scalar containing shellcode for the specified listener.

#### Example

```
$data = stager("my-listener", "x86");

$handle = openf(">out.bin");
writeb($handle, $data);
closef($handle);```

