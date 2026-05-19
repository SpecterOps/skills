bof_extract

The function extracts the executable code for the specified entry point from the Beacon Object File (BOF) and is typically used in conjunction with the BEACON_SLEEP_MASK hook.

#### Arguments

`$1` - A string containing the beacon object file.

`$2` - Entry point of the code to extract. The default is "sleep_mask"

#### Returns

The extracted BOF.

#### Example

```
set BEACON_SLEEP_MASK {
  local('$beacon_type $arch $type $handle $data $bof $bof_len');
  ($beacon_type, $arch) = @_;
  $type = "";
  if ($beacon_type ne "default") {
    $type = "_ $+ $beacon_type";
  }
 
  $handle = openf(script_resource("sleepmask $+ $type $+ . $+ $arch $+ .o"));
  $data = readb($handle, -1);
  closef($handle);

  $bof = bof_extract($data, "sleep_mask");
  $bof_len = strlen($bof);

  if ($bof_len <= 0) {
     return %(status => 0, result => $null, error => "Error: failed to extract the sleepmask BOF.");
  }
  return %(status => 1, result => $bof, information => "Sleepmask BOF generated. Total size: $bof_len");
}```

