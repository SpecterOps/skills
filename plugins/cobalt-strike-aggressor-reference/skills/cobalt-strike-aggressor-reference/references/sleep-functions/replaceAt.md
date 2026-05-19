# replaceAt

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/replaceAt.html

---

## Synopsis

```sleep
$ replaceAt("string", "new", index, [n])
```

Replaces n characters starting at the specified index with the new string.

## Parameters

`"string"` - the string to replace text in.

`"new"` - the new string to insert into the "string".

`index` - the index to insert the new string into

`n` - number of characters to remove starting at the index (defaults to length of "new")

## Returns

A scalar string.

## Examples

**Example:**
```sleep
$string = "this is a test, really";
$string = replaceAt($string, "drill", 10, 4);

println($string);

```

**Output:**
```
this is a drill, really

```

## See Also

[&replace](replace.md); [&strrep](strrep.md)
