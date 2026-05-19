# ohasha

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/ohasha.html

---

## Synopsis

```sleep
% ohasha(key => value, ...)
```

Creates an ordered Sleep hash. All keys are stored in access order from least to most recently accessed.

## Parameters

`key => value` - a key/value pair to populate the hash with.

`...` - any number of key/value pairs may be specified.

## Returns

An ordered hash

## Side Effects / Notes

- New values are placed into the hash. Changing the value of a key will not change insertion order.

- Each individual key access against this ordered hash will result in a change in key order.

## Examples

**Example:**
```sleep
%random = %(a => "apple", b => "boy", c => "cat", d => "dog");
println("Random: " . %random);

%ordered = ohasha(a => "apple", b => "boy", c => "cat", d => "dog");
println("Ordered: " . %ordered);

println("Accessing 'a': " . %ordered['a']);
println("Ordered: " . %ordered);

```

**Output:**
```
Random: %(d => 'dog', a => 'apple', c => 'cat', b => 'boy')
Ordered: %(a => 'apple', b => 'boy', c => 'cat', d => 'dog')
Accessing 'a': apple
Ordered: %(b => 'boy', c => 'cat', d => 'dog', a => 'apple')

```

## See Also

[&ohash](ohash.md); [&setMissPolicy](setMissPolicy.md); [&setRemovalPolicy](setRemovalPolicy.md)
