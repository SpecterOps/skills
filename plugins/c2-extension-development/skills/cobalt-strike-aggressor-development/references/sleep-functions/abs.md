# abs

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/abs.html

---

## Synopsis

```sleep
$ abs(n)
```

Calculate the absolute value of the argument.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$par1 = 10.25;
$par2 = -20;

$a = abs(10.25);
$b = abs(-30);
$c = abs("45");

println($a);
println($b);
println($c);

```

**Output:**
```
10.25
30.0
45.0

```

## See Also

[&ceil](ceil.md); [&floor](floor.md); [&round](round.md)
