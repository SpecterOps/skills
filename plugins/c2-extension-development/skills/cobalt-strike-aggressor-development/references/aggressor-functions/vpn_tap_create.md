vpn_tap_create

Create a Covert VPN interface on the team server system.

#### Arguments

`$1` - the interface name (e.g., phear0)

`$2` - the MAC address ($null will make a random MAC address)

`$3` - reserved; use $null for now.

`$4` - the port to bind the VPN's channel to

`$5` - the type of channel [bind, http, icmp, reverse, udp]

#### Example

```
vpn_tap_create("phear0", $null, $null, 7324, "udp");```
