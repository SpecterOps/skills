# let

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/let.html

---

## Synopsis

```sleep
& let(&closure, $key => "value", ...)
```

Updates the specified closure's environment with all of the key/value pair arguments. Returns the specified closure.

## Parameters

`&closure` - the closure to update the "this" scope for.

`$key => value` - sets $key in the this scope of the specified closure to the right hand side value.

`$this => &closure2` - if a $this is specified, then the resulting closure will share its this scope with &closure2

## Returns

The specified &closure

## Side Effects / Notes

- Updates the specified closure's this scope.

## Examples

**Example:**
```sleep
$foo = { println("My favorite is $icecream with $topping"); };
let($foo, $icecream => "mint chocolate chip",
$topping => "sprinkles");
[$foo];
let($foo, $topping => "strawberries"); # update $foo with a new $topping
[$foo];

```

**Output:**
```
My favorite is mint chocolate chip with sprinkles
My favorite is mint chocolate chip with strawberries

```

## See Also

[&compile_closure](compile_closure.md); [&lambda](lambda.md)
