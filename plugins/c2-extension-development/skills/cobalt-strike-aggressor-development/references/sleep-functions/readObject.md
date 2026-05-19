# readObject

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readObject.html

---

## Synopsis

```sleep
$ readObject([$handle])
```

reads a serialized scalar back from the specified handle

## Parameters

`$handle` - the handle to read from (defaults to stdin/stdout)

## Returns

the scalar read back in from the handle. $null is returned in the event there is any trouble.

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

[&bread](bread.md); [&readAll](readAll.md); [&readb](readb.md); [&readc](readc.md); [&readln](readln.md); [&setEncoding](setEncoding.md)
