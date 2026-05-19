transform

Transform shellcode into another format.

#### Arguments

`$1` - the shellcode to transform

`$2` - the transform to apply

| Description |  |
| --- | --- |
| comma separated byte values |  |
| Hex-encode the value |  |
| PowerShell.exe-friendly base64 encoder |  |
| a VBA array() with newlines added in |  |
| a VBS expression that results in a string |  |
| Veil-ready string (\x##\x##) |  |

#### Returns

The shellcode after the specified transform is applied

#### Example

```
println(transform("This is a test!", "veil"));```

