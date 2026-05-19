# eval

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/eval.html

---

## Synopsis

```sleep
$ eval("code")
```

Parses and evaluates the specified sleep code returning the value of the code.

## Parameters

`"code"` - a string containing the statements to evaluate.

## Returns

The result of the statements once parsed and evaluated.

## Side Effects / Notes

- The statements could have any effect on the environment.

## Errors

- Throws [sleep.error.YourCodeSucksException](../docs/api/sleep/error/YourCodeSucksException.md) in the presence of a syntax error

## Examples

**Example:**
```sleep
$x = 5;
$cond = '$x < 8';
eval('while ('.$cond.') {
println("val: $x");
$x++;
}');

```

**Output:**
```
val: 5
val: 6
val: 7

```

## See Also

[&compile_closure](compile_closure.md); [&expr](expr.md)
