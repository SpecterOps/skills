# search

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/search.html

---

## Synopsis

```sleep
$ search(@array, &closure, [index])
```

Applies the specified &closure to each element of the specified array until a non-$null value is returned.

## Parameters

`@array` - the array to search through

`&closure` - the function to apply to each element of the second argument. Each call to &closure has an argument containing the current index value of the search as $1

`index` - the index to start searching from (optional argument defaults to 0).

## Returns

The search stops when the specified closure returns a value other than $null. This value is returned by the search function.

## Examples

**Example:**
```sleep
@array = @("apple", "apes", "bats", "bars", "beer", "girls");

sub criteria
{
println("Looking at $1");
return iff(charAt($1, 0) ne "a", "found $1", $null);
}

$answer1 = search(@array, &criteria);
println("And... $answer1");

$answer2 = search(@array, &criteria, 4);
println("we have... $answer2");

```

**Output:**
```
Looking at apple
Looking at apes
Looking at bats
And... found bats
Looking at beer
we have... found beer

```

## See Also

[&filter](filter.md); [&map](map.md); [&reduce](reduce.md)
