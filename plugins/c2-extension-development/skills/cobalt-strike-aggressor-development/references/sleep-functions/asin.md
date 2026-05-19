# asin

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/asin.html

---

## Synopsis

```sleep
$ asin(n)
```

Calculate the arc sine of the argument. (answer in radians)

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$value = asin(0.5);
println("arcsine of 0.5 is $value radians");

$value = degrees(asin(0.5));
println("arcsine of 0.5 is $value degrees");

```

**Output:**
```
arcsine of 0.5 is 0.5235987755982989 radians
arcsine of 0.5 is 30.000000000000004 degrees

```

## See Also

[&acos](acos.md); [&atan](atan.md); [&atan2](atan2.md); [&cos](cos.md); [&sin](sin.md); [&tan](tan.md)
