# mark

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/mark.html

---

## Synopsis

```sleep
mark([$handle], n)
```

marks the current point in this IO stream. a buffer is created allowing the mark to be [&reset](reset.md) until n bytes has been reached.

## Parameters

`$handle` - the handle to mark

`n` - the number of bytes to buffer (to allow for a reset back to this mark later) (default is a 10KB buffer)

## Side Effects / Notes

- marks the current point in this stream and creates a buffer to back all reads until the stream is reset.

- only one mark can exist per stream. calling this function destroys the previous mark information.

## Examples

**Example:**
```sleep
$buffer = allocate();
writeb($buffer, "this.is.an.example");
closef($buffer);

println("Read: " . readb($buffer, 4));
mark($buffer);

println("Read: " . readb($buffer, 4));
reset($buffer);

println("Read: " . readb($buffer, -1));

```

**Output:**
```
Read: this
Read: .is.
Read: .is.an.example

```

## See Also

[&available](available.md); [&closef](closef.md); &consume; [&printEOF](printEOF.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&skip](skip.md); [&wait](wait.md)
