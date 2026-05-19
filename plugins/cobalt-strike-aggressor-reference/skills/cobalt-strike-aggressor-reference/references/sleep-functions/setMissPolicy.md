# setMissPolicy

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/setMissPolicy.html

---

## Synopsis

```sleep
setMissPolicy(%ohash, &closure)
```

Sets the miss policy for an ordered hash. The miss policy is called when a key with no associated value is requested. The ordered hash is then populated with the value returned by the miss policy closure.

## Parameters

`%ohash` - the ordered hash to set the miss policy for

`&closure` - the miss policy closure.
When called, the closure receives the following arguments:

ArgumentDescription
$1the ordered hash scalar
$2the original key (before string conversion)

## Side Effects / Notes

- Sets the miss policy for the ordered hash. Each ordered hash is allowed only one miss policy. Use $null to set an empty miss policy.

## Examples

**Example:**
```sleep
# Memoization with Miss Policies: Fibonacci Sequence

sub fib
{
local('%fhash');
%fhash = ohash(0 => 0L, 1 => 1L);

setMissPolicy(%fhash,
{
return $1[$2 - 1] + $1[$2 - 2];
});

return %fhash[$1];
}

println("fib[90]: " . fib(90L));

```

**Output:**
```
fib[90]: 2880067194370816120

```

## See Also

[&ohash](ohash.md); [&ohasha](ohasha.md); [&setRemovalPolicy](setRemovalPolicy.md)
