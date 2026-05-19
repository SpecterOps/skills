# sortd

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sortd.html

---

## Synopsis

```sleep
@ sortd(@array)
```

Sorts the specified array in numerical order as double values.

## Parameters

`@array` - the array to sort

## Returns

A reference to the sorted @array.

## Side Effects / Notes

- The specified array is sorted in place if and only if it is a non-read only array. If the array is read-only a copy is made and the elements are then sorted.

## Examples

**Example:**
```sleep
@array = @(3.4, 9.1, 3.2, 8.5, 7);
@sorted = sortd(@array);

println(@sorted);

```

**Output:**
```
@(3.2, 3.4, 7, 8.5, 9.1)

```

## See Also

[<=>](spaceship.md); [cmp](cmp.md); [&sort](sort.md); [&sorta](sorta.md); [&sortn](sortn.md)
