# push

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/push.html

---

## Synopsis

```sleep
$ push(@array, $value, ...)
```

Adds the specified values to the end of the specified array.

## Parameters

`@array` - the array to push values on to.

`$value` - a value to add to the end of the specified array.

`...` - any number of $values to add to the array may be specified

## Returns

The first value pushed on to the specified array.

## Examples

**Example:**
```sleep
@stack = @("bottom", "middle", "top");
$top = push(@stack, "top+1", "top+2");

println($top);
println("Stack is: " . @stack);

```

**Output:**
```
top+2
Stack is: @('bottom', 'middle', 'top', 'top+1', 'top+2')

```

## See Also

[&add](add.md); [&pop](pop.md); [&putAll](putAll.md); [&shift](shift.md)
