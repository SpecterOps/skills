# ticks

**Category:** DateTime

**Source:** https://sleep.dashnine.org/manual/ticks.html

---

## Synopsis

```sleep
$ ticks()
```

obtain the current time in milliseconds

## Returns

the number of milliseconds since midnight, January 1, 1970 UTC.

## Examples

**Example:**
```sleep
$start = ticks();

sub fact
{
return iff($1 == 0, 1, $1 * fact($1 - 1));
}

println("100! is: " . fact(100.0));

$time = (ticks() - $start) / 1000.0;
println("Calculation took $time seconds");

```

**Output:**
```
100! is: 9.33262154439441E157
Calculation took 0.015 seconds

```

## See Also

[&formatDate](formatDate.md); [&parseDate](parseDate.md)
