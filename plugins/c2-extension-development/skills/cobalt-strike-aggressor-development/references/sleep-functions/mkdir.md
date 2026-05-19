# mkdir

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/mkdir.html

---

## Synopsis

```sleep
$ mkdir("directory/subdirectory/...")
```

Creates the specified directory.

## Parameters

`"directory/subdirectory/..."` - the path to create, will create the paths as needed if one of them doesn't already exist.

## Returns

The path if the operation was successful or $null.

## Side Effects / Notes

- Hopefully this function creates a directory.

## Examples

**Example:**
```sleep
if (!-exists "/var/www/")
{
mkdir("/var/www/logs");
mkdir("/var/www/htdocs/misc");
mkdir("/var/www/bin");
}

```

## See Also

[-isDir](pr_isDir.md); [&listRoots](listRoots.md); [&ls](ls.md)
