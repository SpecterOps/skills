listener_info

Get information about a listener.

#### Arguments

`$1` - the listener name

`$2` - (optional) the key to extract a value for

#### Returns

```
%info = listener_info("listener-name");```

Returns a dictionary with the metadata for this listener.

```
$value = listener_info("listener-name", "key");```

Returns the value for the specified key from this listener's metadata

#### Example

```
# create a script console alias to dump listener info
command dump {
   println("Listener $1");
   foreach $key => $value (listener_info($1)) {
      println("$[15]key $value");
   }
}```

