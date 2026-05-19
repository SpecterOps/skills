# retainAll

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/retainAll.html

---

## Synopsis

```sleep
@ retainAll(@a, @b)
```

Removes all of the elements of @a not present in @b. This is the set intersection operation on @a and @b.

## Parameters

`@a` - the first array.

`@b` - the second array.

Scalar identity is used to determine scalar equivalence for this function. the identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

## Returns

The array @a

## Side Effects / Notes

- This function modifies the contents of @a by removing the non-intersecting elements of @b.

## Examples

**Example:**
```sleep
@a = @("z", "b", "c", "d", "e");
@b = @("a", "b", "c");

retainAll(@a, @b);

println("@a = " . @a);
println("@b = " . @b);

```

**Output:**
```
@a = @('b', 'c')
@b = @('a', 'b', 'c')

```

## See Also

[=~](identity.md); [in](in.md); [&addAll](addAll.md); [&removeAll](removeAll.md)
