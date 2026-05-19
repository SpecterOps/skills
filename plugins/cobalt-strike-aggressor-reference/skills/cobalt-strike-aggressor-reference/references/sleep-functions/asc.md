# asc

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/asc.html

---

## Synopsis

```sleep
$ asc("c")
```

Returns a scalar integer of the ascii value of the specified character

## Parameters

`"c"` - the character to get the ascii value of.

## Returns

A scalar integer with an ascii value.

## Examples

**Example:**
```sleep
$string = "abcDEF";

for ($x = 0; $x < strlen($string); $x++)
{
$char = charAt($string, $x);
$asc = asc($char);
println("$char = $asc");
}

```

**Output:**
```
a = 97
b = 98
c = 99
D = 68
E = 69
F = 70

```

## See Also

[&chr](chr.md)
