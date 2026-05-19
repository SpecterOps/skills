# cos

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/cos.html

---

## Synopsis

```sleep
$ cos(n)
```

Calculate the cosine of the argument. (answer in radians)

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$value = cos(1.5);
println("cosine of 1.5 radians is $value");

$value = cos(radians(1.5));
println("cosine of 1.5 degrees is $value");

```

**Output:**
```
cosine of 1.5 radians is 0.0707372016677029
cosine of 1.5 degrees is 0.9996573249755573

```

## See Also

[&acos](acos.md); [&asin](asin.md); [&atan](atan.md); [&atan2](atan2.md); [&sin](sin.md); [&tan](tan.md)
