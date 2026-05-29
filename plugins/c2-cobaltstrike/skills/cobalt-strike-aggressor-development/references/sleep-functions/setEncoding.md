# setEncoding

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/setEncoding.html

---

## Synopsis

```sleep
setEncoding($handle, "charset name")
```

sets the character set to encode/decode written/read characters with the specified handle.

## Parameters

`$handle` - the handle to set the encoding for.

`"charset name"` - the unicode character set.

## Returns

A $handle to the file. This handle can be read from and written to using Sleep's IO functions.

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

[&print](print.md); [&printAll](printAll.md); [&println](println.md); [&readAll](readAll.md); [&readc](readc.md); [&readln](readln.md)
