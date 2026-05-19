# removeAll

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/removeAll.html

---

## Synopsis

```sleep
@ removeAll(@a, @b)
```

Removes all of the elements of @b from @a. This is the set difference operation on @a and @b.

## Parameters

`@a` - the first array.

`@b` - the second array.

Scalar identity is used to determine scalar equivalence for this function. the identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

## Returns

The array @a

## Side Effects / Notes

- This function modifies the contents of @a by removing the contents of @b.

## Examples

**Example:**
```sleep
@a = @("z", "b", "c", "d", "e");
@b = @("a", "b", "c");

removeAll(@a, @b);

println("@a = " . @a);
println("@b = " . @b);

```

**Output:**
```
@a = @('z', 'd', 'e')
@b = @('a', 'b', 'c')

```

## See Also

[=~](identity.md); [in](in.md); [&addAll](addAll.md); [&retainAll](retainAll.md)
