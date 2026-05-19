host_update

Add or update a host in the targets model

#### Arguments

`$1` - the IPv4 or IPv6 address of this target [you may specify an array of hosts too]

`$2` - the DNS name of this target

`$3` - the target's operating system

`$4` - the operating system version number (e.g., 10.0)

`$5` - a note for the target.

#### Note

You may specify a `$null` value for any argument and, if the host exists, no change will be made to that value.

#### Example

```
host_update("192.168.20.3", "DC", "Windows", 10.0);```

