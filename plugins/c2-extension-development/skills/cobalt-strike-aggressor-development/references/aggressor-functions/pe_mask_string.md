pe_mask_string

Mask a string in the Beacon DLL Content based on position.

#### Arguments

`$1` - Beacon DLL content

`$2` - Start location

`$3` - Byte value mask key (int)

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_mask_string {

   local('$temp_dll, $location, $length, $maskkey');
   local('%pemap');
   local('@loc);

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
   # Set parameters
   # -------------------------------------
   $location = @loc[0];
   $length = 5;
   $maskkey = 23;

   # -------------------------------------
   # pe_mask_string (mask a string in a dll)
   # -------------------------------------
   # warn("pe_mask_string(dll, " . $location . ", " . $maskkey . ")");
   $temp_dll = pe_mask_string($temp_dll, $location, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # un-mask (running the same mask a second time should "un-mask")
   # we are unmasking the length of the string and the null character
   # (This would normally be done by the reflective loader)
   # -------------------------------------
   # warn("pe_mask(dll, " . $location . ", " . $length . ", " . $maskkey . ")");
   # $temp_dll = pe_mask($temp_dll, $location, $length, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```
