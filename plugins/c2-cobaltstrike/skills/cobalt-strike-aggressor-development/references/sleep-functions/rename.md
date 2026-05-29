# rename

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/rename.html

---

## Synopsis

```sleep
$ rename("old", "new")
```

Rename the specified file.

## Parameters

`"old"` - the old file to rename.

`"new"` - the new file name.

## Returns

The new path if the operation was successful or $null.

## Side Effects / Notes

- Hopefully this function renames the old file :)

## Examples

**Example:**
```sleep
# how to use Sleep to rename thousands of files

$newprefix = "olddata";
$oldprefix = "dota";

sub checkFile
{
if (-isDir $1)
{
map(&checkFile, ls($1));
}
else if ("$oldprefix $+ *.html" iswm $1)
{
rename($1, strrep($1, $oldprefix, $newprefix));
}
}

checkFile("c:/");

```

## See Also

[&createNewFile](createNewFile.md); [&deleteFile](deleteFile.md); [&mkdir](mkdir.md)
