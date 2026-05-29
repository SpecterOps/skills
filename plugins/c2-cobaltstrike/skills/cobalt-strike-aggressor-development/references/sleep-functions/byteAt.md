# byteAt

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/byteAt.html

---

## Synopsis

```sleep
$ byteAt("string", n)
```

Returns the byte at the n'th position in the string

## Parameters

`"string"` - the string to extract the byte value from.

`n` - the string position to extract the byte value from.

## Returns

A scalar integer.

## Examples

**Example:**
```sleep
$string = "hello world";

for ($x = 0; $x < strlen($string); $x++)
{
print(byteAt($string, $x) . " ");
}

println();

```

**Output:**
```
104 101 108 108 111 32 119 111 114 108 100

```

## See Also

[&charAt](charAt.md); [&left](left.md); [&mid](mid.md); [&right](right.md); [&strlen](strlen.md); [&substr](substr.md)
