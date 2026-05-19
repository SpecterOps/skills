# floor

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/floor.html

---

## Synopsis

```sleep
$ floor(n)
```

Rounds the specified value down to the previous integer value.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

An integer scalar.

## Side Effects / Notes

- shouldn't this return a long number?

## Examples

**Example:**
```sleep
$value = 3.57;

$floor = floor($value);
println("floor( $+ $value $+ ): $floor");

```

**Output:**
```
floor(3.57): 3.0

```

## See Also

[&abs](abs.md); [&ceil](ceil.md); [&round](round.md)
