# readln

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readln.html

---

## Synopsis

```sleep
$ readln([$handle])
```

reads a single line of text from the specified handle

## Parameters

`$handle` - the handle to read from (defaults to stdin/stdout)

## Returns

a scalar string with the read text. If no text is read then $null is returned instead.

## Examples

**Example:**
```sleep
$handle = openf("readfile.sl");

while $read (readln($handle))
{
# do something useful.
}

```

## See Also

[&bread](bread.md); [&readAll](readAll.md); [&readb](readb.md); [&readc](readc.md); [&readObject](readObject.md); [&setEncoding](setEncoding.md)
