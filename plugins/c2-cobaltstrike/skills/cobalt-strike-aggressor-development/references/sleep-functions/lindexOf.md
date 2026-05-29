# lindexOf

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/lindexOf.html

---

## Synopsis

```sleep
$ lindexOf("string", "substr", [start])
```

Returns the last index of "substr" inside of "string" counting backwards from the specified start index.

## Parameters

`"string"` - the string to search.

`"substr"` - the substring to search for.

`start` - the position from which to begin the search (default is the end of the string)

## Returns

A scalar integer with the index. A failed search will return $null.

## Examples

**Example:**
```sleep
$last = lindexOf("abcdeab", "a");
println($last);

```

**Output:**
```
5

```

## See Also

[&find](find.md); [&indexOf](indexOf.md)
