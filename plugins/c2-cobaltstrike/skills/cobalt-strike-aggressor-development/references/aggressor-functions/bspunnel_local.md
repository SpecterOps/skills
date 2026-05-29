bspunnel_local

Spawn and tunnel an agent through this Beacon (via a target localhost-only reverse port forward). Note: this reverse port forward tunnel traverses through the Beacon chain to the team server and, via the team server, out through the requesting Cobalt Strike client.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the architecture (e.g., x86, x64)

`$3` - the host of the controller

`$4` - the port of the controller

`$5` - a file with position-independent code to execute in a temporary process.

#### Example

```
bspunnel_local($1, "x64", "127.0.0.1", 4444, script_resource("agent.bin"));```
