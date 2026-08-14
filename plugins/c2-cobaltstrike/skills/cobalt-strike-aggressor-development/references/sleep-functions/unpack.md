# unpack

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/unpack.html

---

## Synopsis

```sleep
@ unpack('format', "string")
```

unpacks data from the specified sleep string. data is returned as a sleep array with each scalar set to a type as specified in the format string

## Parameters

`'format'` - a string describing the number of packed values and their types.

- 8.3 Binary I/O - summary of pack/unpack template characters

`"string"` - a scalar string containing serialized data

## Returns

a scalar array with data reconstituded from the byte string

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

[&bread](bread.md); [&bwrite](bwrite.md); [&pack](pack.md); [&sizeof](sizeof.md)
