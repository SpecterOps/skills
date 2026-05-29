# substr

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/substr.html

---

## Synopsis

```sleep
$ substr("string", start, [end])
```

Extracts a substring of the specified string from the specified start index up to but not including the specified end index.

## Parameters

`"string"` - the string to grab a substring of.

`start` - the start index. (defaults to 0)

`end` - the optional end index, if not specified will default to pulling the rest of the string.

## Returns

The specified substring.

## Examples

**Example:**
```sleep
$string = "abcdefghijklmnopqrstuvwxyz";
$substr = substr($string, 13, 18);

println($substr);

```

**Output:**
```
nopqr

```

## See Also

[&byteAt](byteAt.md); [&charAt](charAt.md); [&left](left.md); [&mid](mid.md); [&right](right.md); [&strlen](strlen.md)
