# bwrite

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/bwrite.html

---

## Synopsis

```sleep
$ bwrite([$handle], 'format', $x, ...)
```

writes data to $handle. each format character corresponds to one or more arguments.

```sleep
$ bwrite([$handle], 'format', @array)
```

writes data to $handle. each format character corresponds to one or more array elements.

## Parameters

`$handle` - an I/O handle to write to (STDOUT is default)

`'format'` - a string describing the number of values to expect and their types.

- 8.3 Binary I/O - summary of pack/unpack template characters

`$x, ...` - an arbitrary piece of data. the pack format describes how many pieces of data to expect and what type to pack them into.

`@array` - an array full of arbitrary pieces of data used by this function.

## Side Effects / Notes

- Writes data to the specified I/O handle

## Examples

**Example:**
```sleep
$handle = openf(">>/var/log/wtmp");

# fake an entry into the wtmp log... better be root to do this.
bwrite($handle, 'Z8 Z8 Z16 I', "tty0", "dritchie", "att.net", ticks() / 1000);

```

## See Also

[&bread](bread.md); [&pack](pack.md); [&sizeof](sizeof.md); [&unpack](unpack.md)
