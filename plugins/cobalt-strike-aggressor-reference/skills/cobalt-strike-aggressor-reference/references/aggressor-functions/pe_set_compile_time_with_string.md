pe_set_compile_time_with_string

Set the compile time in the Beacon DLL Content.

#### Arguments

`$1` - Beacon DLL content

`$2` - Compile Time (as a string)

#### Returns

Updated DLL Content

#### Example

```
# ("01 Jan 2020 15:16:17" = "1577913377000")
$strTime = "01 Jan 2020 15:16:17";
$temp_dll = pe_set_compile_time_with_string($temp_dll, $strTime);```

