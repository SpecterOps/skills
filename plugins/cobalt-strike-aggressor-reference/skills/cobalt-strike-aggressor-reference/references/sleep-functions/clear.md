# clear

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/clear.html

---

## Synopsis

```sleep
clear(@array)
```

Removes all of the contents from @array.

```sleep
clear(%hash)
```

Removes all of the contents from %hash.

## Parameters

`@array, %hash` - the array to remove the contents from

## Side Effects / Notes

- This function clears the contents of the passed in data structure.

## Examples

**Example:**
```sleep
@a = @(1, 2, 3, 4, 5);

clear(@a);

println("@a is: " . @a);

```

**Output:**
```
@a is: @()

```

## See Also

[&add](add.md); [&addAll](addAll.md); [&remove](remove.md); [&removeAt](removeAt.md); [&removeAll](removeAll.md); [&splice](splice.md)
