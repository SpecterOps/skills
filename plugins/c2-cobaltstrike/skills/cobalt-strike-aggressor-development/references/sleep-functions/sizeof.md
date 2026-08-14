# sizeof

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/sizeof.html

---

## Synopsis

```sleep
$ sizeof('format')
```

calculates the size of the data structure specified by the format string.

## Parameters

`'format'` - a string describing the number of values to expect and their types.

- 8.3 Binary I/O - summary of pack/unpack template characters

## Returns

the estimated size (in bytes) of the data

## Examples

**Example:**
```sleep
$handle = openf("/var/log/wtmp");

# read an entry from the wtmp log..

($tty, $uid, $host, $ctime) = bread($handle, 'Z8 Z8 Z16 I');
$date = formatDate($ctime * 1000, "EEE, d MMM yyyy HH:mm:ss Z");

println("$[10]tty $[10]uid $[20]host $date");

```

**Output:**
```
ttyp2 raffi Mon, 13 Apr 2009 18:00:52 -0400

```

## See Also

[&bread](bread.md); [&bwrite](bwrite.md); [&pack](pack.md); [&unpack](unpack.md)
