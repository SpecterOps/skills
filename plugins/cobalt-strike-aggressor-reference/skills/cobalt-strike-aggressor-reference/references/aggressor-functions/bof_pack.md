bof_pack

Pack arguments in a way that's suitable for BOF APIs to unpack.

#### Arguments

`$1` - the id for the Beacon (needed for unicode conversions)

`$2` - format string for the packed data

`...` - one argument per item in our format string

#### Note

This function packs its arguments into a binary structure for use with &beacon_inline_execute. The format string options here correspond to the BeaconData* C API available to BOF files. This API handles transformations on the data and hints as required by each type it can pack.

| Description | Unpack With (C) |  |
| --- | --- | --- |
| binary data | BeaconDataExtract |  |
| 4-byte integer | BeaconDataInt |  |
| 2-byte short integer | BeaconDataShort |  |
| zero-terminated+encoded string | BeaconDataExtract |  |
| zero-terminated wide-char string | (wchar_t *)BeaconDataExtract |  |

The Cobalt Strike documentation has a page specific to BOF files. See *Beacon Object Files*.

See also&beacon_inline_execute

