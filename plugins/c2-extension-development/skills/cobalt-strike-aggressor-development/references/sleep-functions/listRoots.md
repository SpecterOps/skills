# listRoots

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/listRoots.html

---

## Synopsis

```sleep
@ listRoots()
```

Lists all of the root directories.

## Returns

An array of strings with the full paths of all of the root directories in the file system. On Windows this will be c:\, d:\, etc. and on UNIX this will be /

## Examples

**Example:**
```sleep
println("Roots are: " . listRoots());

```

**Output:**
```
Roots are: @('/')

```

## See Also

[-isDir](pr_isDir.md); [&ls](ls.md); [&mkdir](mkdir.md)
