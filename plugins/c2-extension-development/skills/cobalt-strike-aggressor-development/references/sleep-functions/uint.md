# uint

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/uint.html

---

## Synopsis

```sleep
$ uint(n)
```

Interpret the specified value as an unsigned integer

## Parameters

`n` - the value to apply this function to.

## Returns

A long scalar

## Examples

**Example:**
```sleep
$value = uint(-1);
println($value);

```

**Output:**
```
4294967295

```

## See Also

[&cast](cast.md); [&casti](casti.md); [&double](double.md); [&int](int.md); [&long](long.md)
