# atan

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/atan.html

---

## Synopsis

```sleep
$ atan(n)
```

Calculate the arc tangent of the argument. (answer in radians)

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$value = atan(1);
println("arctangent of 1 is $value radians");

$value = degrees(atan(1));
println("arctangent of 1 is $value degrees");

```

**Output:**
```
arctangent of 1 is 0.7853981633974483 radians
arctangent of 1 is 45.0 degrees

```

## See Also

[&acos](acos.md); [&asin](asin.md); [&atan2](atan2.md); [&cos](cos.md); [&sin](sin.md); [&tan](tan.md)
