# pr_eof

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/pr_eof.html

---

## Synopsis

```sleep
-eof $handle
```

A predicate to check if the reader portion of the handle is closed (end of file)

## Parameters

`$handle` - the handle to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
$handle = openf("/etc/hosts");

while (!-eof $handle)
{
$text = readln($handle);
print(".");
}

println("\ndone!");

```

**Output:**
```
.................
done!

```

## See Also

[&closef](closef.md); [&printEOF](printEOF.md)
