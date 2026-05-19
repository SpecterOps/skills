barch

Returns the architecture of your Beacon session (e.g., x86 or x64)

#### Arguments

`$1` - the id for the beacon to pull metadata for

#### Note

If the architecture is unknown (e.g., a DNS Beacon that hasn't sent metadata yet); this function will return x86.

#### Example

```
println("Arch is: " . barch($1));```
