# getFileParent

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/getFileParent.html

---

## Synopsis

```sleep
$ getFileParent("/path/path/file")
```

Extracts the parent path of the specified file/directory

## Parameters

`"/path/path/file"` - the path to operate on.

## Returns

The parent directory of the specified file/directory.

## Examples

**Example:**
```sleep
$path = "/Users/raffi/sleepdev/sleep/readme.txt";
$x = 0;

while $path (getFileParent($path))
{
println((".." x $x) . " $path");
$x++;
}

```

**Output:**
```
/Users/raffi/sleepdev/sleep
.. /Users/raffi/sleepdev
.... /Users/raffi
...... /Users
........ /

```

## See Also

[&getFileName](getFileName.md); [&getFileProper](getFileProper.md)
