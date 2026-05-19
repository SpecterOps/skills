# bread

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/bread.html

---

## Synopsis

```sleep
@ bread([$handle], 'format')
```

reads data from $handle. Returned as a scalar array with types specified by the format string

## Parameters

`$handle` - a handle to read the data in from (defaults to stdin)

`'format'` - a string describing the number of packed values and their types.

- [8.3 Binary I/O](io.md#3) - summary of pack/unpack template characters

## Returns

a scalar array with data reconstituded from the byte string

## Side Effects / Notes

- consumes bytes from the specified handle

## Examples

**Example:**
```sleep
# pack/unpack templates are basically C struct definitions.
# the sizeof operator is meant to provide the size of a chunk of data.

$format = 'Z8 Z8 Z16 I';
println(sizeof($format) . " bytes");

```

**Output:**
```
ttyp4 raffi Fri, 2 May 2008 00:26:45 -0400

```

## See Also

[&bwrite](bwrite.md); [&pack](pack.md); [&sizeof](sizeof.md); [&unpack](unpack.md)
