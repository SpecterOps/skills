pe_insert_rich_header

Insert rich header data into Beacon DLL Content. If there is existing rich header information, it will be replaced.

#### Arguments

`$1` - Beacon DLL content

`$2` - Rich header

#### Returns

Updated DLL Content

#### Note

The rich header length should be on a 4 byte boundary for subsequent checksum calculations.

#### Example

```
# -------------------------------------
# Insert (replace) rich header
# -------------------------------------
$rich_header = "<your rich header info>";
$temp_dll = pe_insert_rich_header($temp_dll, $rich_header);```

