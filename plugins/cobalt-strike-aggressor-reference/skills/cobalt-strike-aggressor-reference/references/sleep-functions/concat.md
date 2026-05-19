# concat

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/concat.html

---

## Synopsis

```sleep
@ concat(@a, @b, [...])
```

Concatenates the specified arrays into one.

## Parameters

`@a, @b` - arrays to join together

`...` - any number of arguments may be specified. non-array arguments are simply added to the resulting array.

## Returns

A new array

## Side Effects / Notes

- this function makes copies of its arguments and none of the passed in data structures are modified.

## Examples

**Example:**
```sleep
@a = @(1, 2, 3);
@b = @("a", "b", "c");

@c = concat(@a, '|', @b, @b);
println(@c);

```

**Output:**
```
@(1, 2, 3, '|', 'a', 'b', 'c', 'a', 'b', 'c')

```

## See Also

[&clear](clear.md); [&flatten](flatten.md); [&reverse](reverse.md); [&sublist](sublist.md); [&splice](splice.md)
