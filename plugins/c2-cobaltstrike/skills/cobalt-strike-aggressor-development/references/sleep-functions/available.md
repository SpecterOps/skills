# available

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/available.html

---

## Synopsis

```sleep
$ available([$handle])
```

Obtain the number of bytes that can be read from handle without blocking.

```sleep
$ available($handle, "delim")
```

Read ahead in the handle to see if the delimeter is present in the buffer or not.

## Parameters

`$handle` - the handle to check. if no handle is specified the console will be used.

`"delim"` - the delimeter to search for.

## Returns

In the first usage, the number of bytes readable from the handle without blocking. In the second case $null is returned if the delimeter is not found. Otherwise the position of the delimeter is returned.

## Side Effects / Notes

- In the delimeter searching usage of this function, the mark and reset values of the handle are utilized.

## Examples

**Example:**
```sleep
$handle = connect("www.yahoo.com", 80);
println($handle, "GET /");
sleep(3000);

println(available($handle) . " bytes are available");

```

**Output:**
```
9562 bytes are available

```

## See Also

[&closef](closef.md); &consume; [&mark](mark.md); [&printEOF](printEOF.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&skip](skip.md); [&wait](wait.md)
