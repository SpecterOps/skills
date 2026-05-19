# strlen

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/strlen.html

---

## Synopsis

```sleep
$ strlen("string")
```

Returns the length of the specified string.

## Parameters

`"string"` - the string to obtain the length of.

## Returns

A scalar integer

## Examples

**Example:**
```sleep
$string = "this is some text";
$length = strlen($string);

println($length);

```

**Output:**
```
17

```

## See Also

[&byteAt](byteAt.md); [&charAt](charAt.md); [&left](left.md); [&mid](mid.md); [&right](right.md); [&substr](substr.md)
