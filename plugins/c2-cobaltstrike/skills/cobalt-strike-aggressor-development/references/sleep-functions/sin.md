# sin

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/sin.html

---

## Synopsis

```sleep
$ sin(n)
```

Calculate the sine of the argument. (answer in radians)

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$temp = sin(30);
println("sin value of 30 radians is $temp");

$temp = sin(radians(30));
println("sin value of 30 degrees is $temp");

```

**Output:**
```
sin value of 30 radians is -0.9880316240928618
sin value of 30 degrees is 0.49999999999999994

```

## See Also

[&acos](acos.md); [&asin](asin.md); [&atan](atan.md); [&atan2](atan2.md); [&cos](cos.md); [&tan](tan.md)
