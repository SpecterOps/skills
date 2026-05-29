# mid

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/mid.html

---

## Synopsis

```sleep
$ mid("string", start, [length])
```

Returns a substring of the specified "string" starting from the start index followed by the next n chars

## Parameters

`"string"` - the string to grab a substring of.

`start` - the start index. (defaults to 0)

`length` - number of characters to grab starting at the start index.

## Returns

The specified substring.

## Examples

**Example:**
```sleep
$string = "abcdefghijklmnopqrstuvwxyz";
$substr = mid($string, 13, 5);

println($substr);

```

**Output:**
```
nopqr

```

## See Also

[&byteAt](byteAt.md); [&charAt](charAt.md); [&left](left.md); [&right](right.md); [&strlen](strlen.md); [&substr](substr.md)
