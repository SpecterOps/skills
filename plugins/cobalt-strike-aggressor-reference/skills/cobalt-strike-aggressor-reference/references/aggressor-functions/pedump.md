pedump

Parse an executable Beacon into a map of the PE Header information. The parsed information can be used for research or programmatically to make changes to the Beacon.

#### Arguments

`$1` - Beacon DLL content

#### Returns

A map of the parsed information. The map data is very similar to the "./peclone dump [file]" command output.

#### Example

```
# ===========================================================================
# 'case insensitive sort' from sleep manual...
# ===========================================================================
sub caseInsensitiveCompare
{
   $a = lc($1);
   $b = lc($2);
   return $a cmp $b;
}

# ===========================================================================
# Dump PE Information
# $1 = Beacon DLL content
# ===========================================================================
sub dump_my_pe {
   local('$out $key $val %pemap @sorted_keys');

   %pemap = pedump($1);

   # ---------------------------------------------------
   # Example listing all items from hash/map...
   # ---------------------------------------------------
   @sorted_keys = sort(&caseInsensitiveCompare, keys(%pemap));
   foreach $key (@sorted_keys)
   {
      $out = "$[50]key";
      foreach $val (values(%pemap, @($key)))
      {
         $out .= " $val";
         println($out);
      }
   }

   # ---------------------------------------------------
   # Example of grabbing specific items from hash/map...
   # ---------------------------------------------------
   local('@loc_cs @val_cs');
   @loc_cs = values(%pemap, @("CheckSum.<location>"));
   @val_cs = values(%pemap, @("CheckSum.<value>"));

   println("");
   println("My DLL CheckSum Location: " . @loc_cs);
   println("My DLL CheckSum Value: " . @val_cs);
   println("");
}```

See also./peclone dump [file]

