pe_set_compile_time_with_long

Set the compile time in the Beacon DLL Content.

#### Arguments

`$1` - Beacon DLL content

`$2` - Compile Time (as a long in milliseconds)

#### Returns

Updated DLL Content

#### Example

```
# date is in milliseconds ("1893521594000" = "01 Jan 2030 12:13:14")
$date = 1893521594000;
$temp_dll = pe_set_compile_time_with_long($temp_dll, $date);

# date is in milliseconds ("1700000001000" = "14 Nov 2023 16:13:21")
$date = 1700000001000;
$temp_dll = pe_set_compile_time_with_long($temp_dll, $date);```
