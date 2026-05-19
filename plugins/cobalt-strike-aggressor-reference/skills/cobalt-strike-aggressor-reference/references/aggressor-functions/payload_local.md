payload_local

Exports a raw payload for a specific Cobalt Strike listener. Use this function when you plan to spawn this payload from another Beacon session. Cobalt Strike will generate a payload that embeds key function pointers, needed to bootstrap the agent, taken from the parent session's metadata.

#### Arguments

`$1` - the parent Beacon session ID

`$2` - the listener name

`$3` - x86|x64 the architecture of the payload

`$4` - exit method: 'thread' (leave the thread when done) or 'process' (exit the process when done). Use 'thread' if injecting into an existing process.

`$5` - A string value for the system call method. Valid values are:

**None**: Use the standard Windows API function.**Direct**: Use the Nt* version of the function.

**Indirect**: Jump to the appropriate instruction within the Nt* version of the function.

`$6` - (optional) The supporting HTTP library for generated beacons (wininet|winhttp|$null|blank string).

#### Returns

A scalar containing position-independent code for the specified listener.

#### Example

```
$data = payload_local($bid, "my-listener", "x86", "process", "None");

$handle = openf(">out.bin");
writeb($handle, $data);
closef($handle);```

