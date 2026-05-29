alias

Creates an alias command in the Beacon console

#### Arguments

`$1` - the alias name to bind to

`$2` - a callback function. Called when the user runs the alias. Arguments are: $0 = command run, $1 = beacon id, $2 = arguments.

#### Example

```
alias("foo", {
   btask($1, "foo!");
});```

#### See Also

*User Defined Tab Completion*
