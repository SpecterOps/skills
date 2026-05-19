pe_set_stringz

Places a string value at a specified location and adds a zero terminator.

#### Arguments

`$1` - Beacon DLL content

`$2` - Start location

`$3` - String to set

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_set_stringz {

   local('$temp_dll, $offset, $value');
   local('%pemap');
   local('@loc');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   %pemap = pedump($temp_dll);
   @loc = values(%pemap, @("Sections.AddressOfName.0."));

   if (size(@loc) != 1) {
      warn("Unexpected size of section name location array: " . size(@loc));
   } else {
      warn("Current section name location: " . @loc[0]);
   }

   # -------------------------------------
   # Set parameters (parse number as base 10)
   # -------------------------------------
   $offset = parseNumber(@loc[0], 10);
   $value = "abc";

   # -------------------------------------
   # pe_set_stringz
   # -------------------------------------
   # warn("pe_set_stringz(dll, " . $offset . ", " . $value . ")");
   $temp_dll = pe_set_stringz($temp_dll, $offset, $value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # Set parameters
   # -------------------------------------
   # $offset = parseNumber(@loc[0], 10);
   # $value = ".tex";

   # -------------------------------------
   # pe_set_string (set a string value)
   # -------------------------------------
   # warn("pe_set_string(dll, " . $offset . ", " . $value . ")");
   # $temp_dll = pe_set_string($temp_dll, $offset, $value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```
