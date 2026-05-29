# splice

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/splice.html

---

## Synopsis

```sleep
@ splice(@array, @insert, [n], [m])
```

removes m elements starting at position n from @array and splices in the contents of @insert.

## Parameters

`@array` - the array to mangle up

`@insert` - the array to insert into @array, a $null value is ok

`n` - the position of @array to splice into, default value is 0

`m` - the number of elements to remove from @array, starting at position n. default value is the size of @insert

## Returns

@array

## Side Effects / Notes

- this function affects @array directly.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", "d", "e");
@insert = @(1, 2, 3);

# start at element 2; remove 1; insert @insert
splice(@array, @insert, 2, 1);

println(@array);

```

**Output:**
```
@('a', 'b', 1, 2, 3, 'd', 'e')

```

## See Also

[&add](add.md); [&removeAt](removeAt.md)
