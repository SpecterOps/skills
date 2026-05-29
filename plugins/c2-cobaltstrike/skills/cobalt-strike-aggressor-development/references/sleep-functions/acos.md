# acos

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/acos.html

---

## Synopsis

```sleep
$ acos(n)
```

Calculate the arc cosine of the argument.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep

$value = acos(-0.5);
println("arccosine of -0.5 is $value radians");

$value = degrees(acos(-0.5));
println("arccosine of -0.5 is $value degrees");

```

**Output:**
```
arccosine of -0.5 is 2.0943951023931957 radians
arccosine of -0.5 is 120.00000000000001 degrees

```

## See Also

[&asin](asin.md); [&atan](atan.md); [&atan2](atan2.md); [&cos](cos.md); [&sin](sin.md); [&tan](tan.md)
