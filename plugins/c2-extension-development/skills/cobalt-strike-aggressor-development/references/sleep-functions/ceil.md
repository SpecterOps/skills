# ceil

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/ceil.html

---

## Synopsis

```sleep
$ ceil(n)
```

Rounds the specified value up to the next integer value.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

An integer scalar.

## Side Effects / Notes

- shouldn't this return a long scalar?

## Examples

**Example:**
```sleep
$value = 3.57;

$ceil = ceil($value);
println("ceil( $+ $value $+ ): $ceil");

```

**Output:**
```
ceil(3.57): 4.0

```

## See Also

[&abs](abs.md); [&floor](floor.md); [&round](round.md)
