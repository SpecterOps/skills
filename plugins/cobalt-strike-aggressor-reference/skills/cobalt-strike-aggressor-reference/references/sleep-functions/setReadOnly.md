# setReadOnly

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/setReadOnly.html

---

## Synopsis

```sleep
$ setReadOnly("file")
```

set the read only attribute of the specified file.

## Parameters

`"file"` - the file to set the read only attribute for.

## Returns

Returns the filename if the operation was successful, otherwise $null is returned.

## Side Effects / Notes

- Sets the specified file to be read only. There is no built-in functionality to undo this attribute.

## Examples

**Example:**
```sleep
createNewFile("blah.txt");

if (-canwrite "blah.txt")
{
print("Yeap, we can write it...");
setReadOnly("blah.txt");
println(" not any more!");
}

$handle = openf(">blah.txt");

if (checkError($error))
{
println("Could not open blah.txt for writing: $error");
}
else
{
println($handle, "wheee");
closef($handle);
}

```

**Output:**
```
Yeap, we can write it... not any more!
Could not open blah.txt for writing: java.io.FileNotFoundException: blah.txt (Permission denied)

```

## See Also

[-canread](pr_canread.md); [-canwrite](pr_canwrite.md)
