# int

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/int.html

---

## Synopsis

```sleep
$ int(n)
```

Convert the specified value to an int scalar

## Parameters

`n` - the value to apply this function to.

## Returns

An int scalar.

## Examples

**Example:**
```sleep
$value = int(12.456);
println("Integer value is $value");

$value = int(-12.456);
println("Integer value is $value");

$value = int(10 / 3);
println("Integer value is $value");

```

**Output:**
```
Integer value is 12
Integer value is -12
Integer value is 3

```

## See Also

[&cast](cast.md); [&casti](casti.md); [&double](double.md); [&long](long.md); [&uint](uint.md)
