pe_set_export_name

Set the export name in the Beacon DLL Content.

#### Arguments

`$1` - Beacon DLL content

#### Returns

Updated DLL Content

#### Note

The name must exist in the string table.

#### Example

```
# -------------------------------------
# name must be in strings table...
# -------------------------------------
$export_name = "WININET.dll";
$temp_dll = pe_set_export_name($temp_dll, $export_name);

$export_name = "beacon.dll";
$temp_dll = pe_set_export_name($temp_dll, $export_name);```

