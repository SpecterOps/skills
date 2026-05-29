# acquire

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/acquire.html

---

## Synopsis

```sleep
acquire($semaphore)
```

blocks the current thread of execution until the semaphore count is > 0, when that happens the semaphore count is decremented.

## Parameters

`$semaphore` - the semaphore to check and decrement

## Side Effects / Notes

- Once the semaphore count is > 0 this function will (in an atomic step) decrement the semaphore.

## Examples

**Example:**
```sleep
%shared = %(produce => semaphore(0),
consume => semaphore(1),
buffer => $null);

sub producer
{
for ($x = 0; $x < 3; $x++)
{
acquire(%shared["consume"]);
println("Produce: $x * 3");
%shared["buffer"] = $x * 3;
release(%shared["produce"]);
}
}

sub consumer
{
for ($y = 0; $y < 3; $y++)
{
acquire(%shared["produce"]);
println("Consume: " . %shared["buffer"]);
release(%shared["consume"]);
}
}

fork(&consumer, \%shared);
fork(&producer, \%shared);

```

**Output:**
```
Produce: 0 * 3
Consume: 0
Produce: 1 * 3
Consume: 3
Produce: 2 * 3
Consume: 6

```

## See Also

[&fork](fork.md); [&release](release.md); [&semaphore](semaphore.md)
