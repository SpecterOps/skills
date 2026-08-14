# closef

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/closef.html

---

## Synopsis

```sleep
closef($handle)
```

Closes the read and write channels for the specified I/O handle

```sleep
closef(port)
```

Locates the specified port in the server socket listen table and closes it

## Parameters

`$handle` - an Object scalar containing a Sleep I/O reference handle.

`port` - the port number to stop listening for connections on

## Examples

**Example:**
```sleep
# overwrite data.txt

$handle = openf(">data.txt");
println($handle, "this is some data.");
closef($handle);

```

## See Also

[&available](available.md); &consume; [&mark](mark.md); [&printEOF](printEOF.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&skip](skip.md); [&wait](wait.md)
