bdllinject

Inject a Reflective DLL into a process.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the PID to inject the DLL into

`$3` - the local path to the Reflective DLL

#### Example

```
bdllinject($1, 1234, script_resource("test.dll"));```

