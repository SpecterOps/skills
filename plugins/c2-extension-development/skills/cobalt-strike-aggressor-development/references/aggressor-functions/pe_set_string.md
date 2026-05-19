pe_set_string

Places a string value at a specified location.

#### Arguments

`$1` - Beacon DLL content

`$2` - Start location

`$3` - Value

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_set_string {

   local('$temp_dll, $location, $value');
   local('%pemap');
   local('@loc_en, @val_en');

   $temp_dll = $1;

   # -------------------------------------
   # Inspect the current DLL...
   # -------------------------------------
   %pemap = pedump($temp_dll);
   @loc_en = values(%pemap, @("Export.Name."));
   @val_en = values(%pemap, @("Export.Name."));

   if (size(@val_en) != 1) {
      warn("Unexpected size of export name value array: " . size(@val_en));
   } else {
      warn("Current export value: " . @val_en[0]);
   }

   if (size(@loc_en) != 1) {
      warn("Unexpected size of export location array: " . size(@loc_en));
   } else {
      warn("Current export name location: " . @loc_en[0]);
   }

   # -------------------------------------
   # Set parameters (parse number as base 10)
   # -------------------------------------
   $location = parseNumber(@loc_en[0], 10);
   $value = "BEECON.DLL";

   # -------------------------------------
   # pe_set_string (set a string value)
   # -------------------------------------
   # warn("pe_set_string(dll, " . $location . ", " . $value . ")");
   $temp_dll = pe_set_string($temp_dll, $location, $value);

   # -------------------------------------
   # Did it work?
   # -------------------------------------
   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```
