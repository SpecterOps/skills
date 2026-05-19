bdllload

Call LoadLibrary() in a remote process with the specified DLL.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the target process PID

`$3` - the on-target path to a DLL

#### Note

The DLL must be the same architecture as the target process.

#### Example

```
bdllload($1, 1234, "c:\\windows\\mystuff.dll");```

