# checksum

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/checksum.html

---

## Synopsis

```sleep
$ checksum("string", 'algorithm')
```

Returns (as a scalar long) the checksum of the specified byte string using the specified algorithm.

```sleep
$ checksum($handle, '[>]algorithm')
```

Sets up the specified handle so that all reads (or if the algorithm is prefixed with >, writes) are checksummed using the specified algorithm. Returns a $checksum object that can be used to obtain the final digest value.

```sleep
$ checksum($checksum)
```

Returns (as a scalar long) the checksum of the handle associated with $checksum.

## Parameters

`"string"` - a string of bytes to checksum the data from

`$handle` - the I/O handle to attach a checksum object to.

`$checksum` - an object scalar referencing a checksum object.

`'algorithm'` -
the algorithm to use when checksumming the data.

AlgorithmDescription
Adler32Adler-32 Checksum Algorithm; faster than CRC32, less reliable
CRC32Cyclid Redundancy Check Algorithm

## Returns

This is dependent on the form used. The checksum values themselves are all scalar longs.

## Examples

**Example:**
```sleep
# generate a CRC32 sum from any file.

sub crc32
{
$handle = openf($1);
$digest = checksum($handle, "CRC32");

# consume the handle
skip($handle, lof($1));

closef($handle);

$result = checksum($digest);
println(formatNumber($result, 10, 16));
}

crc32(@ARGV[0]);

```

**Output:**
```
$ java -jar sleep.jar checksum.sl checksum.sl
29452c1b
$ crc32 checksum.sl
29452c1b

```

## See Also

[&digest](digest.md)
