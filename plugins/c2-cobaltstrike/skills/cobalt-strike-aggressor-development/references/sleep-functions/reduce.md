# reduce

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/reduce.html

---

## Synopsis

```sleep
$ reduce(@|&, &closure)
```

Applies &closure to the first two elements of the specified array or closure. The resulting value is then applied to the next value of the specified array or closure, so on and so forth. Returns one value.

## Parameters

`@|&` - this argument can be an array or a closure. if an array is specified the array is considered done when it returns $null.

`&closure` - the function to apply to each element of the specified array or closure.

## Returns

A single scalar value that is a reduction of the specified closure or array.

## Examples

**Example:**
```sleep
@a = @(99, 8, 7, 65, 100, 33);

# calculate the minimum value of @a

$min = reduce({ return iff($1 < $2, $1, $2); }, @a);

println("The minimum value of @a is: $min");

```

**Output:**
```
The minimum value of @a is: 7

```

## See Also

[&filter](filter.md); [&map](map.md); [&search](search.md)
