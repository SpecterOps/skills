# setLastModified

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/setLastModified.html

---

## Synopsis

```sleep
$ setLastModified("file", time)
```

set the last modified time of the specified file.

## Parameters

`"file"` - the file to set the last modified time of.

`time` - the new modified time of the file specified as a scalar long in milliseconds since the epoch.

## Returns

Returns the filename if the operation was successful, otherwise $null is returned.

## Side Effects / Notes

- Sets the last modified time of the specified file.

## Examples

**Example:**
```sleep
# yes Professor, I submitted the homework on time, look at the timestamp.

$oneDayAgo = lastModified("homework.tgz") - (24 * ((60 * 1000) * 60));
setLastModified("homework.tgz", $oneDayAgo);

```

## See Also

[&lastModified](lastModified.md)
