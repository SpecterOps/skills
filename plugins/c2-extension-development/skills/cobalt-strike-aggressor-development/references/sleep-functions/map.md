# map

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/map.html

---

## Synopsis

```sleep
@ map(&closure, @|&)
```

Applies the specified closure to each element of the second argument and returns an array of all return values.

## Parameters

`&closure` - the function to apply to each element of the second argument. $1 is the current element.

`@|&` - the famed second argument, this can be an array or another closure. If a closure is specified the closure will be called continuously until $null is returned.

## Returns

An array with all of the return values of the first function applied to each individual element of the second argument.

## Examples

**Example:**
```sleep
@array = @("cows", "chickens", "dogs", 3);
@results = map({ return "$1 :)"; }, @array);

println(@results);

```

**Output:**
```
@('cows :)', 'chickens :)', 'dogs :)', '3 :)')

```

## See Also

[&filter](filter.md); [&reduce](reduce.md); [&search](search.md)
