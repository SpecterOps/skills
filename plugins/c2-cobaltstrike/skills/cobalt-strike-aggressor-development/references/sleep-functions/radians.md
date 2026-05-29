# radians

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/radians.html

---

## Synopsis

```sleep
$ radians(n)
```

Converts the angle n measured in degrees to an approximately equivalent angle in radians.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$convert = radians(45) / [Math PI];
println("45 degrees is $convert / Pi radians");

$convert = radians(720) / [Math PI];
println("720 degrees is $convert / Pi radians");

```

**Output:**
```
45 degrees is 0.25 / Pi radians
720 degrees is 4.0 / Pi radians

```

## See Also

[&degrees](degrees.md)
