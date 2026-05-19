# writeObject

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/writeObject.html

---

## Synopsis

```sleep
writeObject([$handle], $scalar, ...)
```

serializes and writes all of the scalar arguments out to the specified handle

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`$scalar` - a scalar to serialize into bytes

`...` - any number of the scalars can be specified

## Side Effects / Notes

- data serialized with this function can be reconstitude with [&readObject](readObject.md)

- Sleep functions are serializable. However due to a limitation in Java. If a foreach loop is in progress, the function will not serialize. Thanks Sun!

## Examples

**Example:**
```sleep
sub a
{
@data = @("a", "b", "c");
writeObject($source, @data);

@stuff = @(1, 2, 3);
writeObject($source, @stuff);
}

$handle = fork(&a);

@a = readObject($handle);
println("Read array: " . @a);

@b = readObject($handle);
println("Read array: " . @b);

```

**Output:**
```
Read array: @('a', 'b', 'c')
Read array: @(1, 2, 3)

```

## See Also

[&bwrite](bwrite.md); [&print](print.md); [&printAll](printAll.md); [&println](println.md); [&writeb](writeb.md)
