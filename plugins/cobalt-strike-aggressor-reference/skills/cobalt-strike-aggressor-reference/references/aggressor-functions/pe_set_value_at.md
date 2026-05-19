pe_set_value_at

Sets a long value based on the location resolved by a name from the PE Map (see pedump).

#### Arguments

`$1` - Beacon DLL content

`$2` - Name of location field

`$3` - Value

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = DLL content
# ===========================================================================
sub demo_pe_set_value_at {

   local('$temp_dll, $name, $long_value, $date');
   local('%pemap');
   local('@loc, @val');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   # %pemap = pedump($temp_dll);
   # @loc = values(%pemap, @("SizeOfImage."));
   # @val = values(%pemap, @("SizeOfImage."));

   # if (size(@val) != 1) {
   #   warn("Unexpected size of SizeOfImage. value array: " . size(@val));
   # } else {
   #   warn("Current SizeOfImage. value: " . @val[0]);
   # }

   # if (size(@loc) != 1) {
   #   warn("Unexpected size of SizeOfImage location array: " . size(@loc));
   # } else {
   #   warn("Current SizeOfImage. location: " . @loc[0]);
   # }

   # -------------------------------------
   # Set parameters
   # -------------------------------------
   $name = "SizeOfImage";
   $long_value = 22334455;

   # -------------------------------------
   # pe_set_value_at (set a long value at the location resolved by name)
   # -------------------------------------
   # $1 = DLL (byte array)
   # $2 = name (string)
   # $3 = value (long)
   # -------------------------------------
   warn("pe_set_value_at(dll, " . $name . ", " . $long_value . ")");
   $temp_dll = pe_set_value_at($temp_dll, $name, $long_value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # set it back?
   # -------------------------------------
   # warn("pe_set_value_at(dll, " . $name . ", " . @val[0] . ")");
   # $temp_dll = pe_set_value_at($temp_dll, $name, @val[0]);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

