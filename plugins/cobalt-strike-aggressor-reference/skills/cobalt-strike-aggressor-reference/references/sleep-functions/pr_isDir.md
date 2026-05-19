# pr_isDir

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_isDir.html

---

## Synopsis

```sleep
-isDir "file"
```

A predicate to check if a file is a directory

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
if (-isDir "/etc/")
{
println("It is a directory :)");
}

```

**Output:**
```
It is a directory :)

```

## See Also

[-exists](pr_exists.md); [-isFile](pr_isFile.md); [-isHidden](pr_isHidden.md); [&lof](lof.md)
