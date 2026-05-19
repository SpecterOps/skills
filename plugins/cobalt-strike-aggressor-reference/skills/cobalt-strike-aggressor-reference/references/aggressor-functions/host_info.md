host_info

Get information about a target.

#### Arguments

`$1` - the host IPv4 or IPv6 address

`$2` - [Optional] the key to extract a value for

#### Returns

```
%info = host_info("address");```

Returns a dictionary with known information about this target.

```
$value = host_info("address", "key");```

Returns the value for the specified key from this target's entry in the data model.

#### Example

```
# create a script console alias to dump host info
command host {
   println("Host $1");
   foreach $key => $value (host_info($1)) {
      println("$[15]key $value");
   }
}```

