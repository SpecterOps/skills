# cwd

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/cwd.html

---

## Synopsis

```sleep
$ cwd()
```

returns the current working directory.

## Returns

The current working directory.

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

[&chdir](chdir.md)
