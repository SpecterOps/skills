# writeAsObject

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/writeAsObject.html

---

## Synopsis

```sleep
writeAsObject([$handle], $object, ...)
```

serializes and writes all the object representations of the scalar arguments out to the specified handle

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`$scalar` - an object scalar to serialize into bytes

`...` - any number of object scalars can be specified

## Side Effects / Notes

- data serialized with this function can be reconstitude with [&readAsObject](readAsObject.md)

- this function is similiar to [&writeObject](writeObject.md) except no Scalar wrapper is involved. Use this function when you want to communicate Java objects to a non-sleep app.

## Examples

**Example:**
```sleep
# sleep can interoperate with Java servers by serializing objects
# and sending them over a channel...

$handle = connect("127.0.0.1", 9998);

$list = [new LinkedList];
# do some stuff to $list

# write a java.util.LinkedList to $handle
writeAsObject($handle, $list);

# read an object in.
$object = readAsObject($handle);

```

## See Also

[&bwrite](bwrite.md); [&print](print.md); [&printAll](printAll.md); [&println](println.md); [&writeb](writeb.md); [&writeObject](writeObject.md)
