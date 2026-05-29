# expr

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/expr.html

---

## Synopsis

```sleep
$ expr("expr")
```

Parses and evaluates the specified sleep expression code returning the value of the expression.

## Parameters

`"expr"` - a string containing the expression to evaluate.

## Returns

The result of the expression once parsed and evaluated.

## Side Effects / Notes

- The expression could have any effect on the environment.

## Errors

- Throws a [sleep.error.YourCodeSucksException](../docs/api/sleep/error/YourCodeSucksException.md) in the presence of a syntax error

## See Also

[&compile_closure](compile_closure.md); [&eval](eval.md)
