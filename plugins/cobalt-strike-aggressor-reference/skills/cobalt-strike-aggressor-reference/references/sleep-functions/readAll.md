# readAll

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readAll.html

---

## Synopsis

```sleep
@ readAll([$handle])
```

reads all lines of text from the specified handle and places them into an array

## Parameters

`$handle` - the handle to read from

## Returns

a sleep array containing all of the lines of text read

## Examples

**Example:**
```sleep
$handle = openf("/etc/passwd");
@data = readAll($handle);
closef($handle);

println("Number of entries: " . size(@data));

```

**Output:**
```
Number of entries: 37

```

## See Also

[&bread](bread.md); [&readb](readb.md); [&readc](readc.md); [&readln](readln.md); [&readObject](readObject.md); [&setEncoding](setEncoding.md)
