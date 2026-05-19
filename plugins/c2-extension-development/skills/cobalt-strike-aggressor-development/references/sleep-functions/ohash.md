# ohash

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/ohash.html

---

## Synopsis

```sleep
% ohash(key => value, ...)
```

Creates an ordered Sleep hash. All keys are stored in insertion order.

## Parameters

`key => value` - a key/value pair to populate the hash with.

`...` - any number of key/value pairs may be specified.

## Returns

An ordered hash

## Side Effects / Notes

- New values are placed into the hash. Changing the value of a key will not change insertion order.

## Examples

**Example:**
```sleep
%random = %(a => "apple", b => "boy", c => "cat", d => "dog");
println("Random: " . %random);

%ordered = ohash(a => "apple", b => "boy", c => "cat", d => "dog");
println("Ordered: " . %ordered);

```

**Output:**
```
Random: %(d => 'dog', a => 'apple', c => 'cat', b => 'boy')
Ordered: %(a => 'apple', b => 'boy', c => 'cat', d => 'dog')

```

## See Also

[&ohasha](ohasha.md); [&setMissPolicy](setMissPolicy.md); [&setRemovalPolicy](setRemovalPolicy.md)
