# getFileProper

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/getFileProper.html

---

## Synopsis

```sleep
$ getFileProper("path", "file", ...)
```

Concatenates all arguments into a single coherent path with appropriate separators.

## Parameters

`"path"` - the path to start with

`"file"` - a file or subpath to concatenate to the first path

`...` - as many other subpaths/filenames as you like

## Returns

The path resulting from all arguments joined together.

## Examples

**Example:**
```sleep
$path = getFileProper("/Users/raffi/", "fizz", "buzz/", "foo.txt");
println($path);

```

**Output:**
```
/Users/raffi/fizz/buzz/foo.txt

```

## See Also

[&getFileName](getFileName.md); [&getFileParent](getFileParent.md)
