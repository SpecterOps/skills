# sleep

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/sleep.html

---

## Synopsis

```sleep
sleep(n)
```

Blocking call that forces the current executing thread to sleep for n milliseconds

## Parameters

`n` - number of milliseconds to sleep for.

## Examples

**Example:**
```sleep
$start = ticks();
sleep(2 * 1000); # sleep for 2 seconds
$elapsed = (ticks() - $start) / 1000.0;
println("Elapsed time is: $elapsed seconds");

```

**Output:**
```
Elapsed time is: 2.001 seconds

```

## See Also

[&wait](wait.md)
