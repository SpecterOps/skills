# createNewFile

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/createNewFile.html

---

## Synopsis

```sleep
$ createNewFile("file")
```

Creates an empty file at the specified file location.

## Parameters

`"file"` - the name of the file to create.

## Returns

The filename if the operation was successful or $null.

## Side Effects / Notes

- Hopefully this function creates a file.

## Errors

- An error message will be available if the file creation fails for some reason.

## Examples

**Example:**
```sleep
createNewFile("/private/etc/some_file");

if (checkError($error))
{
println("Unable to create file: $error");
}

```

**Output:**
```
Unable to create file: java.io.IOException: Permission denied

```

## See Also

[&deleteFile](deleteFile.md); [&mkdir](mkdir.md); [&rename](rename.md)
