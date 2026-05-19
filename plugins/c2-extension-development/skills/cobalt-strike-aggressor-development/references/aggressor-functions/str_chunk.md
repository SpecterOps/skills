str_chunk

Chunk a string into multiple parts

#### Arguments

`$1` - the string to chunk

`$2` - the maximum size of each chunk

#### Returns

The original string split into multiple chunks

#### Example

```
# hint... :)
else if ($1 eq "template.x86.ps1") {
   local('$enc');
   $enc = str_chunk(base64_encode($2), 61);
   return strrep($data, '%%DATA%%', join("' + '", $enc));
}```
