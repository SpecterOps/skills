str_decode

Convert a string of bytes to text with the specified encoding.

#### Arguments

`$1` - the string to decode

`$2` - the encoding to use.

#### Returns

The decoded text.

#### Example

```
# convert back to a string we can use (from UTF16-LE)
$text = str_decode($string, "UTF16-LE");```

