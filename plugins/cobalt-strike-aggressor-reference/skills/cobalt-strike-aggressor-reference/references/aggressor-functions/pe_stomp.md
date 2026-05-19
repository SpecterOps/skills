pe_stomp

Set a string to null characters. Start at a specified location and sets all characters to null until a null string terminator is reached.

#### Arguments

`$1` - Beacon DLL content

`$2` - Start location

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_stomp {

   local('$temp_dll, $offset, $value, $old_name');
   local('%pemap');
   local('@loc, @val');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   %pemap = pedump($temp_dll);
   @loc = values(%pemap, @("Sections.AddressOfName.1."));
   @val = values(%pemap, @("Sections.AddressOfName.1."));

   if (size(@val) != 1) {
      warn("Unexpected size of Sections.AddressOfName.1 value array: " . size(@val));
   } else {
      warn("Current Sections.AddressOfName.1 value: " . @val[0]);
   }

   if (size(@loc) != 1) {
      warn("Unexpected size of Sections.AddressOfName.1 location array: " . size(@loc));
   } else {
      warn("Current Sections.AddressOfName.1 location: " . @loc[0]);
   }

   # -------------------------------------
   # Set parameters (parse number as base 10)
   # -------------------------------------
   $location = parseNumber(@loc[0], 10);

   # -------------------------------------
   # pe_stomp (stomp a string at a location)
   # -------------------------------------
   # warn("pe_stomp(dll, " . $location . ")");
   $temp_dll = pe_stomp($temp_dll, $location);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

