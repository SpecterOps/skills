# invoke

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/invoke.html

---

## Synopsis

```sleep
$ invoke(&closure, @args, ["message"], [key => value, ...])
```

Dynamically invokes the specified closure. Allows programatic specification of arguments, key/value pairs, and the message parameter.

## Parameters

`&closure` - the closure to invoke.

`@args` - an array to use as the argument source to pass to the closure.

`"message"` - the $0 i.e. message parameter for the closure.

`key => value` - an option to set against the invoked function.

`$this => &closure2` - if a $this is specified, then the closure invocation will use the this scope of &closure2

`parameters => %hash` - if the parameters key is specified, then the right hand side hash will be used as the source of all named arguments passed to the &closure.

## Returns

The return value of the invocation.

## Errors

- None per [&invoke](invoke.md). However errors from the function invocation occur as normal.

## Examples

**Example:**
```sleep
sub foo {
println("Hello: $name $+ , I got your message $0");
println("The sum of $1 + $2 is: " . ($1 + $2));
}

invoke(&foo, @(3, 45), "call mother",
parameters => %($name => "Raffi"));

```

**Output:**
```
Hello: Raffi, I got your message call mother
The sum of 3 + 45 is: 48

```

## See Also

[&function](function.md); [&inline](inline.md); [&setf](setf.md)
