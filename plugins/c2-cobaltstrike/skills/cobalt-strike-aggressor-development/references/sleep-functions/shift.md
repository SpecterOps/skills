# shift

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/shift.html

---

## Synopsis

```sleep
$ shift(@array)
```

Removes the first element from @array and returns it.

## Parameters

`@array` - the array to "shift" a value from.

## Returns

The scalar removed from the specified array.

## Side Effects / Notes

- This function removes the first element from the specified array.

## Examples

**Example:**
```sleep
@queue = @("bottom", "middle", "top");
$bottom = shift(@queue);

println($bottom);
println("Queue is: " . @queue);

```

**Output:**
```
bottom
Queue is: @('middle', 'top')

```

## See Also

[&add](add.md); [&pop](pop.md); [&push](push.md); [&putAll](putAll.md)
