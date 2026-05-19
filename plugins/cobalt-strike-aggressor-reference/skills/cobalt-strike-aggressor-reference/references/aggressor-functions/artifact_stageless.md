artifact_stageless

DEPRECATED This function is deprecated in Cobalt Strike 4.0. Use &artifact_payload instead.

Generates a stageless artifact (exe, dll) from a (local) Cobalt Strike listener

#### Arguments

`$1` - the listener name (must be local to this team server)

`$2` - the artifact type

`$3` - x86|x64 - the architecture of the generated payload (stage)

`$4` - proxy configuration string

`$5` - callback function. This function is called when the artifact is ready. The `$1` argument is the stageless content.

| Description |  |
| --- | --- |
| an x86 DLL |  |
| an x64 DLL |  |
| a plain executable |  |
| a powershell script |  |
| a python script |  |
| raw payload stage |  |
| a service executable |  |

#### Notes

- This function provides the stageless artifact via a callback function. This is necessary because Cobalt Strike generates payload stages on the team server.
- The proxy configuration string is the same string you would use with **Payloads -> Windows Stageless Payload**. `*direct*` ignores the local proxy configuration and attempts a direct connection. `protocol://user:[email protected]:port` specifies which proxy configuration the artifact should use. The `username` and `password` are optional (e.g., `protocol://host:port` is fine). The acceptable protocols are `socks` and `http`. Set the proxy configuration string to `$null` or `""` to use the default behavior. Custom dialogs may use &drow_proxyserver to set this.
- This function cannot generate artifacts for listeners on other team servers. This function also cannot generate artifacts for foreign listeners. Limit your use of this function to local listers with stages only. Custom dialogs may use &drow_listener_stage to choose an acceptable listener for this function.
- Note: while the Python artifact in Cobalt Strike is designed to simultaneously carry an x86 and x64 payload; this function will only populate the script with the architecture argument specified as `$3`

#### Example

```
sub ready {
   local('$handle');
   $handle = openf(">out.exe");
   writeb($handle, $1);
   closef($handle);
}

artifact_stageless("my-listener", "exe", "x86", "", &ready);```

