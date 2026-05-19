# reset

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/reset.html

---

## Synopsis

```sleep
reset([$handle])
```

resets this IO stream back to the last [&mark](mark.md)

## Parameters

`$handle` - the handle to reset the mark for

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

[&available](available.md); [&closef](closef.md); [&consume](consume.md); [&mark](mark.md); [&printEOF](printEOF.md); [&setEncoding](setEncoding.md); [&skip](skip.md); [&wait](wait.md)
