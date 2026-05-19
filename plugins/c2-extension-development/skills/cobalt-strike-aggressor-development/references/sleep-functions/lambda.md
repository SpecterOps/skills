# lambda

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/lambda.html

---

## Synopsis

```sleep
& lambda(&closure, [$key => "value", ...])
```

Copies &closure into a new closure. The new closure environment is initialized with all of the specified key/value pair arguments.

## Parameters

`&closure` - the closure to copy into a new instance.

`$key => value - sets $key in the this scope of the new closure to the right hand side value.!!this` -

`...` - any number of `$key => value` pairs may be specified.

## Returns

A new closure.

## Examples

**Example:**
```sleep
$myfunc = lambda({ println("foo! $x"); $x++; }, $x => 0);
[$myfunc];
[$myfunc];

```

**Output:**
```
foo! 0
foo! 1

```

## See Also

[&compile_closure](compile_closure.md); [&let](let.md)
