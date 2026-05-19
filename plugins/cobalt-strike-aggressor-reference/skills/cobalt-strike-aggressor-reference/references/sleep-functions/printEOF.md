# printEOF

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/printEOF.html

---

## Synopsis

```sleep
printEOF([$handle])
```

signals EOF (End of File) on the far end by shutting down output for $handle

## Parameters

`$handle` - the handle to close writes to.

## Examples

**Example:**
```sleep
$handle = fork(
{
# do some long drawn out calculation.
$x = 3 * 4;
printEOF($source);
println("...");
});

println("Letting fork do its thing.");
readb($handle);
println("Done.");

```

**Output:**
```
...
Letting fork do its thing.
Done.

```

## See Also

[&available](available.md); [&closef](closef.md); [&consume](consume.md); [&mark](mark.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&skip](skip.md); [&wait](wait.md)
