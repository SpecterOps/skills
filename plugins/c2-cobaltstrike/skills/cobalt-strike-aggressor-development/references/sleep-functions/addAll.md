# addAll

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/addAll.html

---

## Synopsis

```sleep
@ addAll(@a, @b)
```

Adds all of the non-present elements of @b into @a. Essentially this function computes the union of @ and @b.

## Parameters

`@a` - the first array.

`@b` - the second array.

Scalar identity is used to determine scalar equivalence for this function. the identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

## Returns

The array @a

## Side Effects / Notes

- This function modifies the contents of @a by inserting the contents of @b.

## Examples

**Example:**
```sleep
@a = @("a", "b", "c", "x", "y", "z");
@b = @("c", "d", "e", "f");

addAll(@a, @b);

println("@a is: " . @a);

```

**Output:**
```
@a is: @('a', 'b', 'c', 'x', 'y', 'z', 'd', 'e', 'f')

```

## See Also

[=~](identity.md); [in](in.md); [&removeAll](removeAll.md); [&retainAll](retainAll.md)
