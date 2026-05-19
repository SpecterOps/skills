vpn_interface_info

Get information about a VPN interface.

#### Arguments

`$1` - the interface name

`$2` - [Optional] the key to extract a value for

#### Returns

```
%info = vpn_interface_info("interface");```

Returns a dictionary with the metadata for this interface.

```
$value = vpn_interface_info("interface", "key");```

Returns the value for the specified key from this interface's metadata

#### Example

```
# create a script console alias to interface info
command interface {
   println("Interface $1");
   foreach $key => $value (vpn_interface_info($1)) {
      println("$[15]key $value");
   }
}```

