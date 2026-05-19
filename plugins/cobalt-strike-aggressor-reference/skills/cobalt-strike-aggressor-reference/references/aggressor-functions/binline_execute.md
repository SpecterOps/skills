binline_execute

Execute a Beacon Object File. This is the same as using the inline-execute command in Beacon.

#### Arguments

`$1` - the id for the Beacon

`$2` - the path to the BOF file

`$3` - the string argument to pass to the BOF file

`$4` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Notes

This functions follows the behavior of *inline-execute* in the Beacon console. The string argument will be zero-terminated, converted to the target encoding, and passed as an argument to the BOF's go function. To execute a BOF, with more control, use &beacon_inline_execute

The Cobalt Strike documentation has a page specific to BOF files. See *Beacon Object Files*.

