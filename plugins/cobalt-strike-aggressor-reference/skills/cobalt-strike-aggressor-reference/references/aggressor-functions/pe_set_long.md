pe_set_long

Places a long value at a specified location.

#### Arguments

`$1` - Beacon DLL content

`$2` - Location

`$3` - Value

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_set_long {

   local('$temp_dll, $int_offset, $long_value');
   local('%pemap');
   local('@loc_cs, @val_cs');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   %pemap = pedump($temp_dll);
   @loc_cs = values(%pemap, @("CheckSum.<location>"));
   @val_cs = values(%pemap, @("CheckSum.<value>"));

   if (size(@val_cs) != 1) {
      warn("Unexpected size of checksum value array: " . size(@val_cs));
   } else {
      warn("Current checksum value: " . @val_cs[0]);
   }

   if (size(@loc_cs) != 1) {
      warn("Unexpected size of checksum location array: " . size(@loc_cs));
   } else {
      warn("Current checksum location: " . @loc_cs[0]);
   }

   # -------------------------------------
   # Set parameters (parse number as base 10)
   # -------------------------------------
   $int_offset = parseNumber(@loc_cs[0], 10);
   $long_value = 98765;

   # -------------------------------------
   # pe_set_long (set a long value)
   # -------------------------------------
   # warn("pe_set_long(dll, " . $int_offset . ", " . $long_value . ")");
   $temp_dll = pe_set_long($temp_dll, $int_offset, $long_value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

