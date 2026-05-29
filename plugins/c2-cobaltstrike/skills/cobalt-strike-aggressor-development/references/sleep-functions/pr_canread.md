# pr_canread

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_canread.html

---

## Synopsis

```sleep
-canread "file"
```

A predicate to check if a file is readable

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
if (!-canread "/etc/shadow")
{
println("Looks like I can not read the shadow file");
}

```

**Output:**
```
Looks like I can not read the shadow file

```

## See Also

[-canwrite](pr_canwrite.md); [&setReadOnly](setReadOnly.md)
