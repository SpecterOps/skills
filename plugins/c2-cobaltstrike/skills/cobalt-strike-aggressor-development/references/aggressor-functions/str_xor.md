str_xor

Walk a string and XOR it with the provided key.

#### Arguments

`$1` - the string to mask

`$2` - the key to use (string)

#### Returns

The original string masked with the specified key.

#### Example

```
$mask  = str_xor("This is a string", "key");
$plain = str_xor($mask, "key");```
