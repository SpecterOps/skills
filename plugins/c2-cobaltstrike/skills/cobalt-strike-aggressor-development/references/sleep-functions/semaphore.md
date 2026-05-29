# semaphore

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/semaphore.html

---

## Synopsis

```sleep
$ semaphore(initial_count)
```

Creates a counting semaphore suitable for use with acquire and release. A semaphore is a synchronization primitive used to protect critical sections of code.

## Parameters

`initial_count` - the initial value of the semaphore. Default value is 1 (a binary semaphore).

## Returns

A new Semaphore object.

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

[&acquire](acquire.md); [&fork](fork.md); [&release](release.md)
