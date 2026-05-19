# atan2

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/atan2.html

---

## Synopsis

```sleep
$ atan2(n, m)
```

Calculate the arc tangent of angle n / m.

## Parameters

`n` - the value (converted to a double) to apply this function to.

`m` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$y = 30;
$x = 60;

$value = atan2 ($y, $x);

println("atan2 of 30/60 is : $value");

```

**Output:**
```
atan2 of 30/60 is : 0.4636476090008061

```

## See Also

[&acos](acos.md); [&asin](asin.md); [&atan](atan.md); [&cos](cos.md); [&sin](sin.md); [&tan](tan.md)
