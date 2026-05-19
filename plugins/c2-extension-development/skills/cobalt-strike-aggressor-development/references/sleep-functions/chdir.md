# chdir

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/chdir.html

---

## Synopsis

```sleep
$ chdir("directory")
```

changes the current working directory to the specified directory.

## Parameters

`"directory"` - the directory to act as the current working directory

## Side Effects / Notes

- Sets the current working directory. This effects [&openf](openf.md), [&exec](exec.md), and all file system bridge operations. [&fork](fork.md) also inherits this value.

## Examples

**Example:**
```sleep
chdir("/etc");
println(cwd());

$handle = openf("passwd");

```

**Output:**
```
/etc

```

## See Also

[&cwd](cwd.md)
