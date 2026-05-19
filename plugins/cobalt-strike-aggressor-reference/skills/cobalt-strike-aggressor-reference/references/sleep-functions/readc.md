# readc

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readc.html

---

## Synopsis

```sleep
$ readc([$handle])
```

reads a single unicode character from the specified handle

## Parameters

`$handle` - the handle to read from (defaults to stdin/stdout)

## Returns

a scalar string with the character read. If no character is read then $null is returned instead.

## Examples

**Example:**
```sleep
$handle = openf("data.cp437.txt");
setEncoding($handle, "cp437");
println("Read: " . readc($handle));

```

**Output:**
```
Read: a

```

## See Also

[&bread](bread.md); [&readAll](readAll.md); [&readb](readb.md); [&readln](readln.md); [&readObject](readObject.md); [&setEncoding](setEncoding.md)
