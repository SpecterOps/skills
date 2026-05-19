listener_describe

Describe a listener.

#### Arguments

`$1` - the listener name

`$2` - (optional) the remote target the listener is destined for

#### Returns

A string describing the listener

#### Example

```
foreach $name (listeners()) {
   println("$name is: " . listener_describe($name));
}```

