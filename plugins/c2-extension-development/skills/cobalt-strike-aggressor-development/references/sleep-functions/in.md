# in

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/in.html

---

## Synopsis

```sleep
? $a in @array
```

Determine if a scalar with identity $a is contained in @array.

```sleep
? "key" in %hash
```

Determine if "key" is in %hash in a read-only way

## Parameters

`$a` - scalar identity to find in @array.
Scalar identity is used to determine scalar equivalence for this function. the identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

`@array` - data structure to search through.

`%hash` - a hash to check for the presence of a key

`"key"` - the key to check for.

## Side Effects / Notes

- Use this function when you want to test if a key is in a hash. Using `%hash["unknownKey"]` will add `"unknownKey"` to %hash with a value of $null

## Examples

**Example:**
```sleep
@a = @("a", "b", "3.0", 2, 3, 4);

$check = iff("3" in @a, "true", "false");
println("a) $check");

$check = iff(3.0 in @a, "true", "false");
println("b) $check");

$check = iff(4.0 in @a, "true", "false");
println("c) $check");

$check = iff("b" in @a, "true", "false");
println("d) $check");

```

**Output:**
```
a) true
b) true
c) false
d) true

```

## See Also

[=~](identity.md); [&addAll](addAll.md); [&removeAll](removeAll.md); [&retainAll](retainAll.md)
