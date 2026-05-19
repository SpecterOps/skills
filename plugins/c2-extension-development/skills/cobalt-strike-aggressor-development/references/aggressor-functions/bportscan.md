bportscan

Ask Beacon to run its port scanner.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the targets to scan (e.g., 192.168.12.0/24)

`$3` - the ports to scan (e.g., 1-1024,6667)

`$4` - the discovery method to use (arp|icmp|none)

`$5` - the max number of sockets to use (e.g., 1024)

`$6 `- (optional) the PID to inject the port scanner into or $null

`$7 `- (optional) the architecture of the target PID (x86|x64) or $null

`$8` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Example

Spawn a temporary process```
bportscan($1, "192.168.12.0/24", "1-1024,6667", "arp", 1024);```

Inject into the specified process```
bportscan($1, "192.168.12.0/24", "1-1024,6667", "arp", 1024, 1234, "x64");```
