# setf

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/setf.html

---

## Synopsis

```sleep
setf('&function', &closure)
```

Binds a closure to the specified function name.

## Parameters

`'&function'` - a string consisting of a function name to bind the closure to.

`&closure` - the closure to bind to the specified function name. A value of $null will remove the function binding.

## Side Effects / Notes

- Adds/changes the binding of a global function name.

## Examples

**Example:**
```sleep
sub foo {
println("foo!");
}

setf('&foo', { println("bar!"); });
foo();

```

**Output:**
```
bar!

```

## See Also

[&function](function.md); [&inline](inline.md); [&invoke](invoke.md)
