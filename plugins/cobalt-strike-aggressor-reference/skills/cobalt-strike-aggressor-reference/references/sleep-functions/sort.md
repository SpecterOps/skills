# sort

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sort.html

---

## Synopsis

```sleep
@ sort(&closure, @array)
```

Sorts the specified array using the specified closure for comparisons.

## Parameters

`&closure` - the comparison function to use.
When called, the closure will have the two values to compare in the $1 and $2 variables. Based on the comparison of $1 and $2 the closure should do one of the following:

ComparisonReturn Value
$1 < $2return a positive value
$2 == $2return 0
$1 > $2return a negative value

`@array` - the array to sort

## Returns

A reference to the sorted @array.

## Side Effects / Notes

- The specified array is sorted in place if and only if it is a non-read only array. If the array is read-only a copy is made and the elements are then sorted.

## Examples

**Example:**
```sleep
sub caseInsensitiveCompare
{
$a = lc($1);
$b = lc($2);

return $a cmp $b;
}

@array = @("zebra", "Xanadu", "ZooP", "ArDvArKS", "Arks", "bATS");
@sorted = sort(&caseInsensitiveCompare, @array);

println(@sorted);

```

**Output:**
```
@('ArDvArKS', 'Arks', 'bATS', 'Xanadu', 'zebra', 'ZooP')

```

## See Also

[<=>](spaceship.md); [cmp](cmp.md); [&sorta](sorta.md); [&sortd](sortd.md); [&sortn](sortn.md)
