# removeAt

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/removeAt.html

---

## Synopsis

```sleep
removeAt(@arrray, index, ...)
```

removes the element located at index from @array.

```sleep
removeAt(%hash, "index", ...)
```

removes the element associated with "index" from %hash.

## Parameters

`@array, %hash` - the data structure to remove the referenced elements from

`index, ...` - the location of the data to remove.

## Side Effects / Notes

- this function will modify the passed in data structure directly.

## Examples

**Example:**
```sleep
%data = %(a => "apple", b => "boy george", c => 33, p => 'pHEAR');
removeAt(%data, "b", "c");

println(%data);

```

**Output:**
```
%(a => 'apple', p => 'pHEAR')

```

## See Also

[&add](add.md); [&addAll](addAll.md); [&remove](remove.md); [&removeAll](removeAll.md); [&splice](splice.md)
