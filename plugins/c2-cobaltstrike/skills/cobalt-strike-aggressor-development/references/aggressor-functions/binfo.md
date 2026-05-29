binfo

Get information from a Beacon session's metadata.

#### Arguments

`$1` - the id for the beacon to pull metadata for

`$2` - the key to extract

#### Returns

A string with the requested information.

#### Example

```
println("User is: " . binfo("1234", "user"));
println("PID  is: " . binfo("1234", "pid"));```
