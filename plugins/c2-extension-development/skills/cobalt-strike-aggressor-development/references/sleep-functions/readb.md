# readb

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/readb.html

---

## Synopsis

```sleep
$ readb([$handle], n)
```

reads n bytes from $handle. If 0 bytes are read $null will be returned.

```sleep
$ readb([$handle], -1, [est_size])
```

reads bytes from handle until none are left. Returns $null when 0 bytes are read.

## Parameters

`$handle` - the handle to read from (defaults to stdin/stdout)

`n` - number of bytes to attempt to read

`est_size` - estimated number of bytes. larger numbers may help performance.

## Returns

a scalar string containing all of the bytes read. If 0 bytes are read $null is returned instead.

## Examples

**Example:**
```sleep
# copy.sl [original file] [new file]

$in = openf(@ARGV[0]);
$data = readb($in, -1);

$out = openf(">" . @ARGV[1]);
writeb($out, $data);

closef($in);
closef($out);

```

## See Also

[&bread](bread.md); [&readAll](readAll.md); [&readc](readc.md); [&readln](readln.md); [&readObject](readObject.md); [&setEncoding](setEncoding.md)
