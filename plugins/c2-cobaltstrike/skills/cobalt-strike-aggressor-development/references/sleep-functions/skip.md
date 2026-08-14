# skip

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/skip.html

---

## Synopsis

```sleep
$ skip($handle, n, [buffer size])
```

reads and discards up to n bytes from the specified handle. this is useful for causing data to be read and processed without the expensive conversion process to sleep strings (i.e. when one wants to [&digest](digest.md) or [&checksum](checksum.md) a file)

## Parameters

`$handle` - the handle to consume bytes from

`n` - the number of bytes to consume

`buffer size` - the size of the byte buffer for consuming bytes, this value can affect performance. default is 32KB.

## Returns

The number of bytes consumed. If no bytes were consumed or an error occured then $null is returned.

## Side Effects / Notes

- consumes bytes from the specified handle.

## Examples

**Example:**
```sleep
# generate an MD5 digest of any file.

sub md5
{
$handle = openf($1);
$digest = digest($handle, "MD5");

# consume the handle
skip($handle, lof($1));

closef($handle);

$result = unpack("H*", digest($digest))[0];
println("MD5 ( $+ $1 $+ ) = $result");
}

md5(@ARGV[0]);

```

**Output:**
```
MD5 (digest.sl) = ff4ddf4a2006140f8db28904de9e288b

```

## See Also

[&available](available.md); [&closef](closef.md); &consume; [&mark](mark.md); [&printEOF](printEOF.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&wait](wait.md)
