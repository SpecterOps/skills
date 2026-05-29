pe_patch_code

Patch code in the Beacon DLL Content based on find/replace in '.text' section'.

#### Arguments

`$1` - Beacon DLL content

`$2` - byte array to find for resolve offset

`$3` - byte array place at resolved offset (overwrite data)

#### Returns

Updated DLL Content

#### Example

```
# ===========================================================================
# $1 = Beacon DLL content

# ===========================================================================
sub demo_pe_patch_code {

   local('$temp_dll, $findme, $replacement');

   $temp_dll = $1;

   # ====== simple text values ======
   $findme = "abcABC123";
   $replacement = "123ABCabc";

   # warn("pe_patch_code(dll, " . $findme . ", " . $replacement . ")");
   $temp_dll = pe_patch_code($temp_dll, $findme, $replacement);

   # ====== byte array as a hex string ======
   $findme = "\x01\x02\x03\xfc\xfe\xff";
   $replacement = "\x01\x02\x03\xfc\xfe\xff";

   # warn("pe_patch_code(dll, " . $findme . ", " . $replacement . ")");
   $temp_dll = pe_patch_code($temp_dll, $findme, $replacement);

   # dump_my_pe($temp_dll);

   # -------------------------------------
   # All Done!  Give back edited DLL!
   # -------------------------------------
   return $temp_dll;
}```
