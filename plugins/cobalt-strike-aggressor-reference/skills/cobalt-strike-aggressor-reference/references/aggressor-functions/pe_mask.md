pe_mask

Mask data in the Beacon DLL Content based on position and length.

#### Arguments

`$1` - Beacon DLL content

`$2` - Start location

`$3` - Length to mask

`$4` - Byte value mask key (int)

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_mask {

   local('$temp_dll, $start, $length, $maskkey');
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
   $start = parseNumber(@loc_en[0], 10);
   $length = 4;
   $maskkey = 22;

   # -------------------------------------
   # mask some data in a dll
   # -------------------------------------
   # warn("pe_mask(dll, " . $start . ", " . $length . ", " . $maskkey . ")");
   $temp_dll = pe_mask($temp_dll, $start, $length, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # un-mask (running the same mask a second time should "un-mask")
   # (This would normally be done by the reflective loader)
   # -------------------------------------
   # warn("pe_mask(dll, " . $start . ", " . $length . ", " . $maskkey . ")");
   # $temp_dll = pe_mask($temp_dll, $start, $length, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

