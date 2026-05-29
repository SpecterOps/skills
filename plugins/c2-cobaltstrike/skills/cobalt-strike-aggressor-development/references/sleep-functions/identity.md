# identity

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/identity.html

---

## Synopsis

```sleep
? $a =~ $b
```

Determine if two scalars have the same identity (value). Scalar identity is a means of determining if two scalars are equivalent values or not. The identity algorithm compares references for object scalars and function scalars. The string representation is used to compare other scalars.

## Parameters

`$a` - any scalar value

`$b` - any scalar value

## Examples

**Example:**
```sleep
sub foo
{
# ...
}

$var = &foo;

$check = iff("3" =~ 3, "true", "false");
println("a) $check");

$check = iff("3" =~ "3.0", "true", "false");
println("b) $check");

$check = iff(&foo =~ $var, "true", "false");
println("c) $check");

$check = iff("blah" =~ 'blah', "true", "false");
println("d) $check");

```

**Output:**
```
a) true
b) false
c) true
d) true

```

## See Also

[=~](identity.md); [in](in.md); [&addAll](addAll.md); [&removeAll](removeAll.md); [&retainAll](retainAll.md)
