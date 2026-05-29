encode

Obfuscate a position-independent blob of code with an encoder.

#### Arguments

`$1` - position independent code (e.g., shellcode, "raw" stageless Beacon) to apply encoder to

`$2` - the encoder to use

`$3` - the architecture (e.g., x86, x64)

| Description |  |
| --- | --- |
| Alphanumeric encoder (x86-only) |  |
| XOR encoder |  |

#### Notes

- The encoded position-independent blob must run from a memory page that has RWX permissions or the decode step will crash the current process.
- **alpha encoder:** The EDI register must contain the address of the encoded blob. &encode prepends a 10-byte (non-alphanumeric) program to the beginning of the alphanumeric encoded blob. This program calculates the location of the encoded blob and sets EDI for you. If you plan to set EDI yourself, you may remove these first 10 bytes.

#### Returns

A position-independent blob that decodes the original string and passes execution to it.

#### Example

```
# generate shellcode for a listener
$stager = shellcode("my-listener", false "x86");

# encode it.
$stager = encode($stager, "xor", "x86");```
