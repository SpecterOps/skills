# readAsObject

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readAsObject.html

---

## Synopsis

```sleep
$ readAsObject([$handle])
```

reads a serialized object from the specified handle

## Parameters

`$handle` - the handle to read from (defaults to stdin)

## Returns

the object read from the handle. $null is returned in the event there is any trouble.

## Side Effects / Notes

- this function is similiar to [&readObject](readObject.md) except no Scalar wrapper is involved. Use this function when you want to communicate Java objects to a non-sleep app.

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

[&bread](bread.md); [&readAll](readAll.md); [&readb](readb.md); [&readc](readc.md); [&readln](readln.md); [&readObject](readObject.md); [&setEncoding](setEncoding.md)
