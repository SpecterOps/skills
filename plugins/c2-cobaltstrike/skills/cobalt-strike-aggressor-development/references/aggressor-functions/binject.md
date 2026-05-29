binject

Ask Beacon to inject a session into a specific process.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the process to inject the session into

`$3` - the listener to target.

`$4` - the process architecture (x86 | x64)

#### Example

```
binject($1, 1234, "my-listener");```
