# getFileName

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/getFileName.html

---

## Synopsis

```sleep
$ getFileName("/path/file")
```

Extracts the file portion of the specified path

## Parameters

`"/path/file"` - the path to operate on.

## Returns

The file portion of the specified path.

## Examples

**Example:**
```sleep
$path = "c:/Documents and Settings/Raphael.Mudge/Desktop/garbage.txt";
println("file name: " . getFileName($path));

```

**Output:**
```
file name: garbage.txt

```

## See Also

[&getFileParent](getFileParent.md); [&getFileProper](getFileProper.md)
