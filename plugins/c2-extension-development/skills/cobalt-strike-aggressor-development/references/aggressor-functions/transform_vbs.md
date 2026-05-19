transform_vbs

Transform shellcode into a VBS expression that results in a string

#### Arguments

`$1` - the shellcode to transform

`$2` - the maximum length of a plaintext run

#### Notes

- Previously, Cobalt Strike would embed its stagers into VBS files as several `Chr()` calls concatenated into a string.
- Cobalt Strike 3.9 introduced features that required larger stagers. These larger stagers were too big to embed into a VBS file with the above method.
- To get past this VBS limitation, Cobalt Strike opted to use `Chr()` calls for non-ASCII data and runs of double-quoted strings for printable characters.
- This change, an engineering necessity, unintentionally defeated static anti-virus signatures for Cobalt Strike's default VBS artifacts at that time.
- If you're looking for an easy evasion benefit with VBS artifacts, consider adjusting the plaintext run length in your Resource Kit.

#### Returns

The shellcode after this transform is applied

#### Example

```
println(transform_vbs("This is a test!", "3"));```
