# pop

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/pop.html

---

## Synopsis

```sleep
$ pop(@array)
```

Removes the last element from @array and returns it.

## Parameters

`@array` - the array to "pop" a value from.

## Returns

The scalar removed from the end of the specified array.

## Side Effects / Notes

- This function removes the last element from the specified array.

## Examples

**Example:**
```sleep
@stack = @("bottom", "middle", "top");
$top = pop(@stack);

println($top);
println("Stack is: " . @stack);

```

**Output:**
```
top
Stack is: @('bottom', 'middle')

```

## See Also

[&add](add.md); [&push](push.md); [&putAll](putAll.md); [&shift](shift.md)
