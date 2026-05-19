# lof

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/lof.html

---

## Synopsis

```sleep
$ lof("path/file")
```

Obtain the size of the specified file.

## Parameters

`"path/file"` - the file to obtain the size of.

## Returns

A long containing the length of the specified file in bytes.

## Examples

**Example:**
```sleep
println("My file size is: " . lof("lof.sl") . " bytes");

```

**Output:**
```
My file size is: 57 bytes

```

## See Also

[-exists](pr_exists.md); [-isDir](pr_isDir.md); [-isFile](pr_isFile.md); [-isHidden](pr_isHidden.md)
