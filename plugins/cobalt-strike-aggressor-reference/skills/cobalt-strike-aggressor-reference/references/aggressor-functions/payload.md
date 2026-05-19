payload

Exports a raw payload for a specific Cobalt Strike listener.

#### Arguments

`$1` - the listener name

`$2` - x86|x64 the architecture of the payload

`$3` - exit method: 'thread' (leave the thread when done) or 'process' (exit the process when done). Use 'thread' if injecting into an existing process.

`$4` - A string value for the system call method. Valid values are:

**None**: Use the standard Windows API function.**Direct**: Use the Nt* version of the function.

**Indirect**: Jump to the appropriate instruction within the Nt* version of the function.

`$5` - (optional) The supporting HTTP library for generated beacons (wininet|winhttp|$null|blank string).

`$6` - (optional) DNS Comm Mode Override. Use this to change the DNS Comm Mode from the default mode defined in Malleable C2 (dns|dns_over_https|$null|blank string).

#### Returns

A scalar containing position-independent code for the specified listener.

#### Example

```
$data = payload("my-listener", "x86", "process", "Direct");

$handle = openf(">out.bin");
writeb($handle, $data);
closef($handle);```

