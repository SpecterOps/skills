# pack

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/pack.html

---

## Synopsis

```sleep
$ pack('format', $x, ...)
```

packs data into a string of bytes. each format character corresponds to one or more arguments.

```sleep
$ pack('format', @array)
```

packs data into a string of bytes. each format character corresponds to one or more array elements.

## Parameters

`'format'` - a string describing the number of values to expect and their types.

- [8.3 Binary I/O](io.md#3) - summary of pack/unpack template characters

`$x, ...` - an arbitrary piece of data. the pack format describes how many pieces of data to expect and what type to pack them into.

`@array` - an array full of arbitrary pieces of data used by this function.

## Returns

a scalar string containing byte representations of the arguments as specified by the format string.

## Examples

**Example:**
```sleep
# pack a long into an unsigned integer representation
$bytes = pack("I", 3232235777L);

# unpack bytes into 4 unsigned bytes
@bytes = unpack("B4", $bytes);

# print them out :)
println(@bytes);

# for giggles... go in reverse
$bytes = pack("B4", reverse(@bytes));
$value = unpack("I", $bytes);

# print out the value
println($value);

```

**Output:**
```
@(192, 168, 1, 1)
@(3232235777L)

```

## See Also

[&bread](bread.md); [&bwrite](bwrite.md); [&sizeof](sizeof.md); [&unpack](unpack.md)
