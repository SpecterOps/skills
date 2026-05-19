bcovertvpn

Ask Beacon to deploy a Covert VPN client.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the Covert VPN interface to deploy

`$3` - the IP address of the interface [on target] to bridge into

`$4` - (optional) the MAC address of the Covert VPN interface

#### Example

```
bcovertvpn($1, "phear0", "172.16.48.18");```
