# strrep

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/strrep.html

---

## Synopsis

```sleep
$ strrep("string", "old", "new", ...)
```

Replaces occurrences of old with new in string. accepts multiple old, new parameters.

## Parameters

`"string"` - the string to replace text in.

`"old"` - the substring to search for and eliminate.

`"new"` - the new string to replace the old string with.

`...` - multiple pairs of "old", "new" strings can be specified saving multiple calls to this function.

## Returns

A scalar string.

## Examples

**Example:**
```sleep
$string = "this is a test of a island string";
$string = strrep($string, "is", "99");

println($string);

```

**Output:**
```
th99 99 a test of a 99land string

```

## See Also

[&replace](replace.md); [&replaceAt](replaceAt.md)
