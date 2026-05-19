# remove

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/remove.html

---

## Synopsis

```sleep
remove(@array, $scalar, ...)
```

Removes all of the specified values from the array.

```sleep
remove(%hash, $scalar, ...)
```

Removes all of the specified values from the hash.

```sleep
remove()
```

This version of [&remove](remove.md) should only be used within a foreach loop. This form removes the current active element of the foreach loop.

## Parameters

`@array, %hash` - the data structure to remove data from.

`$scalar, ...` - the value to remove.
Scalar identity is used to determine scalar equivalence for this function. the identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

## Side Effects / Notes

- Removes certain values (or key/value pairs) from the specified data structure.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", "3", "blah", 3, 3.0);
remove(@array, 3, "b");

println(@array);

```

**Output:**
```
@('a', 'c', 'blah', 3.0)

```

## See Also

[&add](add.md); [&addAll](addAll.md); [&removeAt](removeAt.md); [&removeAll](removeAll.md); [&splice](splice.md)
