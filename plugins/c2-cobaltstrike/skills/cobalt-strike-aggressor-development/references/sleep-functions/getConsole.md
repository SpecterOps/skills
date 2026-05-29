# getConsole

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/getConsole.html

---

## Synopsis

```sleep
$ getConsole()
```

returns the $handle for stdin/stdout.

## Returns

A $handle to stdin/stdout. This handle can be read from and written to using Sleep's IO functions.

## Examples

**Example:**
```sleep
if (-eof getConsole())
{
println(getConsole(), "The console is open!");
}

```

**Output:**
```
The console is open!

```

## See Also

[&allocate](allocate.md); [&connect](connect.md); [&exec](exec.md); [&fork](fork.md); [&listen](listen.md); [&openf](openf.md); [&setEncoding](setEncoding.md)
