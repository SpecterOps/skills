# allocate

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/allocate.html

---

## Synopsis

```sleep
$ allocate([initial size])
```

allocates a writeable memory buffer. calling closef on the returned buffer turns it into a readable buffer. calling closef on a readable buffer frees the buffer.

## Parameters

`initial size` - the desired initial size of the allocated buffer

## Returns

A $handle to a allocated buffer. This handle can be read from and written to using Sleep's IO functions.

## Side Effects / Notes

- Memory buffers are fast! If there is a need to concatenate lots of data or to manipulate streams of data then buffers are a must.

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
# read the file in
$input = openf(@ARGV[0]);
$data = readb($input, -1);
closef($input);

# encrypt the contents of the file...
$buffer = allocate(strlen($data));

for ($x = 0; $x < strlen($data); $x++) {
writeb($buffer, chr(byteAt($data, $x) ^ 0x34));
}

closef($buffer); # buffer is readable now..
$data = readb($buffer, strlen($data));

# write the file out
$output = openf(">" . @ARGV[0]);
writeb($output, $data);
closef($output);

```

## See Also

[&connect](connect.md); [&exec](exec.md); [&fork](fork.md); [&getConsole](getConsole.md); [&listen](listen.md); [&openf](openf.md); [&setEncoding](setEncoding.md)
