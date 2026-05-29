# sorta

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sorta.html

---

## Synopsis

```sleep
@ sorta(@array)
```

Sorts the specified array alphabetically.

## Parameters

`@array` - the array to sort

## Returns

A reference to the sorted @array.

## Side Effects / Notes

- The specified array is sorted in place if and only if it is a non-read only array. If the array is read-only a copy is made and the elements are then sorted.

## Examples

**Example:**
```sleep
@array = @("bats", "Apples", "rats", "Cats");
@sorted = sorta(@array);

println(@sorted);

```

**Output:**
```
@('Apples', 'Cats', 'bats', 'rats')

```

## See Also

[<=>](spaceship.md); [cmp](cmp.md); [&sort](sort.md); [&sortd](sortd.md); [&sortn](sortn.md)
