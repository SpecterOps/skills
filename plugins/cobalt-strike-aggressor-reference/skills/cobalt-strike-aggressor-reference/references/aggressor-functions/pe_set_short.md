pe_set_short

Places a short value at a specified location.

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
sub demo_pe_set_short {

   local('$temp_dll, $int_offset, $short_value');
   local('%pemap');
   local('@loc, @val');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   %pemap = pedump($temp_dll);
   @loc = values(%pemap, @(".text.NumberOfRelocations."));
   @val = values(%pemap, @(".text.NumberOfRelocations."));

   if (size(@val) != 1) {
      warn("Unexpected size of .text.NumberOfRelocations value array: " . size(@val));
   } else {
      warn("Current .text.NumberOfRelocations value: " . @val[0]);
   }

   if (size(@loc) != 1) {
      warn("Unexpected size of .text.NumberOfRelocations location array: " . size(@loc));
   } else {
      warn("Current .text.NumberOfRelocations location: " . @loc[0]);
   }

   # -------------------------------------
   # Set parameters (parse number as base 10)
   # -------------------------------------
   $int_offset = parseNumber(@loc[0], 10);
   $short_value = 128;

   # -------------------------------------
   # pe_set_short (set a short value)
   # -------------------------------------
   # warn("pe_set_short(dll, " . $int_offset . ", " . $short_value . ")");
   $temp_dll = pe_set_short($temp_dll, $int_offset, $short_value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

