# setRemovalPolicy

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/setRemovalPolicy.html

---

## Synopsis

```sleep
setRemovalPolicy(%ohash, &closure)
```

Sets the removal policy for an ordered hash. The removal policy is called when a new value is added to the hash. The return value of the policy determines wether the last element in the hash should be removed or not.

## Parameters

`%ohash` - the ordered hash to set the miss policy for

`&closure` - the miss policy closure.
When called, the closure receives the following arguments:

ArgumentDescription
$1the ordered hash scalar
$2the key of the last element in the hash (the removal candidate)
$3the value of the last element in the hash

## Side Effects / Notes

- Sets the removal policy for the ordered hash. Each ordered hash is allowed only one removal policy. Use $null to set an empty removal policy.

## Examples

**Example:**
```sleep
sub policy
{
if (size($1) >= 3)
{
println("Removing key: $2 value: $3");
return 1;
}

return 0;
}

%cache = ohasha(a => "apple", b => "bat", c => "cat");
setRemovalPolicy(%cache, &policy);

println(%cache);

println("Access 'a': " . %cache["a"]);
println(%cache);

%cache["d"] = "dog";

println(%cache);

```

**Output:**
```
%(a => 'apple', b => 'bat', c => 'cat')
Access 'a': apple
%(b => 'bat', c => 'cat', a => 'apple')
Removing key: b value: bat
%(c => 'cat', a => 'apple', d => 'dog')

```

## See Also

[&ohash](ohash.md); [&ohasha](ohasha.md); [&setMissPolicy](setMissPolicy.md)
