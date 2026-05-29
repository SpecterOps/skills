# filter

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/filter.html

---

## Synopsis

```sleep
@ filter(&closure, @|&)
```

Applies the specified closure to each element of the second argument and returns an array of all non-$null return values.

## Parameters

`&closure` - the function to apply to each element of the second argument. $1 is the current element.

`@|&` - the famed second argument, this can be an array or another closure. If a closure is specified the closure will be called continuously until $null is returned.

## Returns

An array with all of the non-$null return values of the first function applied to each individual element of the second argument.

## Examples

**Example:**
```sleep
#
# filters out all non-uppercase letter characters.
#

sub uppercase_only
{
return iff(uc($1) eq $1 && -isletter $1, $1, $null);
}

$string = join("", filter(&uppercase_only, split("", "Hello World")));
println("Value is: $string");

```

**Output:**
```
Value is: HW

```

## See Also

[&map](map.md); [&reduce](reduce.md); [&search](search.md)
