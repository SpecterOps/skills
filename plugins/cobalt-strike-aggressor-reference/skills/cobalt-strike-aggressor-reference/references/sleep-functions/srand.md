# srand

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/srand.html

---

## Synopsis

```sleep
srand([number])
```

seed the random number generator with the specified scalar (interpreted as a long)

## Parameters

`number` - the number to seed the random number generator with.

## Examples

**Example:**
```sleep
srand(0x1337);
println("Random: " . rand());

srand(0x1337);
println("Random: " . rand());

```

**Output:**
```
Random: 0.0732580700418014
Random: 0.0732580700418014

```

## See Also

[&rand](rand.md)
