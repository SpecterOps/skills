# lastModified

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/lastModified.html

---

## Synopsis

```sleep
$ lastModified("file")
```

obtain the last modified time of the specified file.

## Parameters

`"file"` - the file to obtain the last modified time of.

## Returns

The last modified time of the specified file as a scalar long in milliseconds since the epoch.

## Examples

**Example:**
```sleep
# yes Professor, I submitted the homework on time, look at the timestamp.

$oneDayAgo = lastModified("homework.tgz") - (24 * ((60 * 1000) * 60));
setLastModified("homework.tgz", $oneDayAgo);

```

## See Also

[&setLastModified](setLastModified.md)
