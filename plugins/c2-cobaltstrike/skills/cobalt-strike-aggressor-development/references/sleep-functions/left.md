# left

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/left.html

---

## Synopsis

```sleep
$ left("string", n)
```

Returns the left n characters of "string"

## Parameters

`"string"` - the string to get the characters from.

`n` - number of characters to grab

## Returns

A scalar string.

## Examples

**Example:**
```sleep
println(left("abcde", 3));

```

**Output:**
```
abc

```

## See Also

[&byteAt](byteAt.md); [&charAt](charAt.md); [&mid](mid.md); [&right](right.md); [&strlen](strlen.md); [&substr](substr.md)
