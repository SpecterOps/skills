# pr_isFile

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_isFile.html

---

## Synopsis

```sleep
-isFile "file"
```

A predicate to check if a file is a file (i.e. not a directory)

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
if (-isFile "/tmp")
{
println("wth?!?");
}

```

## See Also

[-exists](pr_exists.md); [-isDir](pr_isDir.md); [-isHidden](pr_isHidden.md); [&lof](lof.md)
