# charAt

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/charAt.html

---

## Synopsis

```sleep
$ charAt("string", n)
```

Returns the character at the n'th position in the string

## Parameters

`"string"` - the string to extract the character value from.

`n` - the string position to extract the character from.

## Returns

A scalar string containing a single character.

## Examples

**Example:**
```sleep
$string = "hello world";

for ($x = 0; $x < strlen($string); $x++)
{
print(charAt($string, $x) . " ");
}

println();

```

**Output:**
```
h e l l o w o r l d

```

## See Also

[&byteAt](byteAt.md); [&left](left.md); [&mid](mid.md); [&right](right.md); [&strlen](strlen.md); [&substr](substr.md)
