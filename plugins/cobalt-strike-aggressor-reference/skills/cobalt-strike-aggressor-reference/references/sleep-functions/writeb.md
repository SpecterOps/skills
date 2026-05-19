# writeb

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/writeb.html

---

## Synopsis

```sleep
writeb([$handle], "string")
```

writes the bytes contained in "string" to $handle

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`"string"` - the data to write

## Examples

**Example:**
```sleep
# copy.sl [original file] [new file]

$in = openf(@ARGV[0]);
$data = readb($in, -1);

$out = openf(">" . @ARGV[1]);
writeb($out, $data);

closef($in);
closef($out);

```

## See Also

[&bwrite](bwrite.md); [&print](print.md); [&printAll](printAll.md); [&println](println.md); [&writeObject](writeObject.md)
