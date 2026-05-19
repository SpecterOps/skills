artifact_sign

Sign an EXE or DLL file using the code-signer malleable c2 profile setting for the active team server.

#### Arguments

`$1` - the contents of the EXE or DLL file to sign

#### Notes

- This function requires that a code-signing certificate is specified in this server's Malleable C2 profile. If no code-signing certificate is configured, this function will return `$1` with no changes.
- If the Cobalt Strike UI is connected to multiple team servers, the code-signer used is for the active team server which may not be the team server used to generate the artifact.


- **DO NOT** sign an executable or DLL twice. The library Cobalt Strike uses for code-signing will create an invalid (second) signature if the executable or DLL is already signed.

#### Returns

A scalar containing the signed artifact.

#### Example

```
# generate an artifact!
 $data = artifact_payload("my-listener", "exe", "x64", "process", "Indirect");

# sign it.
$data = artifact_sign($data);

# save it
$handle = openf(">out.exe");
writeb($handle, $data);
closef($handle);```
