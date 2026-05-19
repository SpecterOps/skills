pe_mask_section

Mask data in the Beacon DLL Content based on position and length.

#### Arguments

`$1` - Beacon DLL content

`$2` - Section name

`$3` - Byte value mask key (int)

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content
# ===========================================================================
sub demo_pe_mask_section {

   local('$temp_dll, $section_name, $maskkey');
   local('@loc_en, @val_en');

   $temp_dll = $1;

   # -------------------------------------
   # Set parameters
   # -------------------------------------
   $section_name = ".text";
   $maskkey = 23;

   # -------------------------------------
   # mask a section in a dll
   # -------------------------------------
   # warn("pe_mask_section(dll, " . $section_name . ", " . $maskkey . ")");
   $temp_dll = pe_mask_section($temp_dll, $section_name, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # un-mask (running the same mask a second time should "un-mask")
   # (This would normally be done by the reflective loader)
   # -------------------------------------
   # warn("pe_mask_section(dll, " . $section_name . ", " . $maskkey . ")");
   # $temp_dll = pe_mask_section($temp_dll, $section_name, $maskkey);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```

