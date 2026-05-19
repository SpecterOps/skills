fireEvent

Fire an event.

#### Arguments

`$1` - the event name

`...` - the event arguments.

#### Example

```
on foo {
   println("Argument is: $1");
}

fireEvent("foo", "Hello World!");```

