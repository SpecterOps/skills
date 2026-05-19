# indexOf

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/indexOf.html

---

## Synopsis

```sleep
$ indexOf("string", "substr", [start])
```

Returns the index of "substr" inside of "string" starting at the specified start index.

## Parameters

`"string"` - the string to search.

`"substr"` - the substring to search for.

`start` - the position from which to begin the search (default is 0)

## Returns

A scalar integer with the index. A failed search will return $null.

## Examples

**Example:**
```sleep
$string = "this is a test";

$start = 0;
while $index (indexOf($string, " ", $start))
{
println("$start $+ : $+ $index " . substr($string, $start, $index));
$start = $index + 1;
}

println("$start $+ :end " . substr($string, $start));

```

**Output:**
```
0:4 this
5:7 is
8:9 a
10:end test

```

## See Also

[&find](find.md); [&lindexOf](lindexOf.md)
