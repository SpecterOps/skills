on

Register an event handler. This is an alternate to the `on` keyword.

#### Arguments

`$1` - the name of the event to respond to

`$2` - a callback function. Called when the event happens.

#### Example

```
sub foo {
   blog($1, "Foo!");
}

on("beacon_initial", &foo);```

