# compile_closure

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/compile_closure.html

---

## Synopsis

```sleep
& compile_closure("code", ...)
```

Creates a new Sleep closure from the specified string of Sleep code.

## Parameters

`"code"` - a string containing the statements of the function.

`...` - a series of key/value pairs to be installed into the closure environment.

## Returns

The closure built from compiling the specified code.

## Errors

- Throws a [sleep.error.YourCodeSucksException](../docs/api/sleep/error/YourCodeSucksException.md) if there are syntax errors

## Examples

**Example:**
```sleep
$foo = compile_closure('return $1 * $x;', $x => 5);
println("\$foo is $foo");
println('[$foo: 2] - ' . [$foo: 2]);
println('[$foo: 8] - ' . [$foo: 8]);
println('[$foo: 4.3] - ' . [$foo: 4.3]);

```

**Output:**
```
$foo is &closure[eval:0]#73
[$foo: 2] - 10
[$foo: 8] - 40
[$foo: 4.3] - 21.5

```

## See Also

[&eval](eval.md); [&expr](expr.md)
