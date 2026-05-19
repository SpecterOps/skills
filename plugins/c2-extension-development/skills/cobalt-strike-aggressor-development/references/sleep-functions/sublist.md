# sublist

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sublist.html

---

## Synopsis

```sleep
@ sublist(@array, start, [end])
```

Extracts a subset of the specified array from the specified start index up to but not including the specified end index.

## Parameters

`@array` - the list to grab a subset of.

`start` - the start index.

`end` - the optional end index, if not specified will default to the rest of the array.

## Returns

The specified sublist.

## Side Effects / Notes

- The returned sublist serves as a "view" into the parent array. Changes to the sublist will show in the parent.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", @("dd", "ee", "ff"), "g", "h");
@sub = sublist(@array, 2, 4);

# note that an array scalar counts as 1 element.
println(@sub);

# modifications to the sublist also affect the parent.
@sub[1] = "what happened?";
println(@sub);
println(@array);

```

**Output:**
```
@('c', @('dd', 'ee', 'ff'))
@('c', 'what happened?')
@('a', 'b', 'c', 'what happened?', 'g', 'h')

```

## See Also

[&clear](clear.md); [&concat](concat.md); [&flatten](flatten.md); [&reverse](reverse.md); [&splice](splice.md)
