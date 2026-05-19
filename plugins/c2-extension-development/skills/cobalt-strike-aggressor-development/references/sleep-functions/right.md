# right

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/right.html

---

## Synopsis

```sleep
$ right("string", n)
```

Returns the right n characters of "string"

## Parameters

`"string"` - the string to get the characters from.

`n` - number of characters to grab

## Returns

A scalar string.

## Examples

**Example:**
```sleep
$string = "this is a test";
$right = right($string, 4);

println("Right chars are: $right");

```

**Output:**
```
Right chars are: test

```

## See Also

[&byteAt](byteAt.md); [&charAt](charAt.md); [&left](left.md); [&mid](mid.md); [&strlen](strlen.md); [&substr](substr.md)
