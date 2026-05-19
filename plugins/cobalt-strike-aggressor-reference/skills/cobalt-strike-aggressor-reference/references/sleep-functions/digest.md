# digest

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/digest.html

---

## Synopsis

```sleep
$ digest("string", 'algorithm')
```

Returns (as a byte string) the digest of the specified byte string using the specified algorithm.

```sleep
$ digest($handle, '[>]algorithm')
```

Sets up the specified handle so that all reads (or if the algorithm is prefixed with >, writes) are checksummed using the specified algorithm. Returns a $digest object that can be used to obtain the final digest value.

```sleep
$ digest($digest)
```

Returns (as a byte string) the digest of the handle associated with $digest.

## Parameters

`"string"` - a string of bytes to checksum the data from.

`$handle` - the I/O handle to attach a digest object to.

`$digest` - an object scalar referencing a digest object.

`'algorithm'` -
the algorithm to use when calculating a digest of the data.

AlgorithmDescription
MD5widely used cryptographic hash function; produces a 128-bit digest
SHA-1successor to MD5; produces a 160-bit digest

## Returns

This is dependent on the form used. The digest values themselves are all byte strings.

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

**Example:**
```sleep
$PASSWORD = 'd1133275ee2118be63a577af759fc052';

print("Password: ");
$getpass = readln();

$result = unpack("H*", digest($getpass))[0];

if ($result eq $PASSWORD)
{
println("Would you like to play a game?");
println("1. Global Thermo-Nuclear War")
}

```

**Output:**
```
$ java -jar sleep.jar passwd.sl
Password: joshua
Would you like to play a game?
1. Global Thermo-Nuclear War

```

## See Also

[&checksum](checksum.md)
