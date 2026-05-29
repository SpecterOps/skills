# round

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/round.html

---

## Synopsis

```sleep
$ round(n)
```

Rounds the specified value to the nearest integer value.

```sleep
$ round(n, places)
```

Rounds the specified value to the specified number of places.

## Parameters

`n` - the value (converted to a double) to apply this function to.

`places` - the number of places to round to (if specified)

## Returns

A long scalar.

## Examples

**Example:**
```sleep
$round = round(3.68);
println("round(3.68): $round");

$round = round([Math PI], 2);
println("round(" . [Math PI] . ", 2): $round");

```

**Output:**
```
round(3.68): 4
round(3.141592653589793, 2): 3.14

```

## See Also

[&abs](abs.md); [&ceil](ceil.md); [&floor](floor.md)
