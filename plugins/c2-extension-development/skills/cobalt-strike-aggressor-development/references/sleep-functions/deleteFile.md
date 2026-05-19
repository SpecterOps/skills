# deleteFile

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/deleteFile.html

---

## Synopsis

```sleep
$ deleteFile("file")
```

Deletes the specified file/directory.

## Parameters

`"file"` - the name of the file to delete.

## Returns

The filename if the operation was successful or $null.

## Side Effects / Notes

- Hopefully this function deletes the file.

## Examples

**Example:**
```sleep
# format someones hard drive...

sub deleteAll
{
if (-isDir $1)
{
map(&deleteAll, ls($1));
}
deleteFile($1);
}

# I work on a mac by default... .
deleteAll("c:/");

```

## See Also

[&createNewFile](createNewFile.md); [&mkdir](mkdir.md); [&rename](rename.md)
