pe_update_checksum

Update the checksum in the Beacon DLL Content.

#### Arguments

`$1` - Beacon DLL content

#### Returns

Updated DLL Content

#### Note

This should be the last transformation performed.

#### Example

```
# -------------------------------------
# update checksum
# -------------------------------------
$temp_dll = pe_update_checksum($temp_dll);```
