# sortn

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sortn.html

---

## Synopsis

```sleep
@ sortn(@array)
```

Sorts the specified array in numerical order as long values.

## Parameters

`@array` - the array to sort

## Returns

A reference to the sorted @array.

## Side Effects / Notes

- The specified array is sorted in place if and only if it is a non-read only array. If the array is read-only a copy is made and the elements are then sorted.

## Examples

**Example:**
```sleep
@array = @(3, 9, 8, 7, 5);
@sorted = sortn(@array);

println(@sorted);

```

**Output:**
```
@(3, 5, 7, 8, 9)

```

## See Also

[<=>](spaceship.md); [cmp](cmp.md); [&sort](sort.md); [&sorta](sorta.md); [&sortd](sortd.md)
