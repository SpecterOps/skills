all_payloads

Generates all the stageless payloads (in x86 and x64) for all the configured listeners. Use the listeners_stageless aggressor function to see the list that will be used for the active team server.

#### Arguments

`$1` - The folder path to create the payloads in. This folder path must already exist.

`$2` - A boolean value for whether the executable files should be signed.

`$3` – A string value for the system call method. Valid values are:

**None**: Use the standard Windows API function.**Direct**: Use the Nt* version of the function.

**Indirect**: Jump to the appropriate instruction within the Nt* version of the function.

`$4` - (optional) The supporting HTTP library for generated beacons (wininet|winhttp|$null|blank string).

$5 - (optional) DNS Comm Mode Override. Use this to change the DNS Comm Mode from the default mode defined in Malleable C2 (dns|dns_over_https|$null|blank string).

#### Example

```
$folder = all_payloads("/tmp/payloads", 1, "None");
println("Payloads have been saved to $folder");```
