# flatten

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/flatten.html

---

## Synopsis

```sleep
@ flatten(@array)
```

Returns a shallow copy of the specified array flattened to 1-dimension.

## Parameters

`@array` - the array to flatten.

## Returns

A shallow copy of the specified array flattened to 1-dimension.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", @("dd", "ee", "ff", @("ggg", "hhh"), "ii"), "j", "k");
@copy = flatten(@array);

println(@copy);

```

**Output:**
```
@('a', 'b', 'c', 'dd', 'ee', 'ff', 'ggg', 'hhh', 'ii', 'j', 'k')

```

## See Also

[&clear](clear.md); [&concat](concat.md); [&reverse](reverse.md); [&sublist](sublist.md); [&splice](splice.md)
