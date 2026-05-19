# add

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/add.html

---

## Synopsis

```sleep
@ add(@array, $scalar, [position])
```

Inserts a scalar into an array at a certain position.

```sleep
@ add(%hash, key => value, ...)
```

Adds any number of key/value pairs to the specified hash.

## Parameters

`@array|%hash` - the data structure to add data to.

`$scalar` - the data to be copied and added to the specified array.

`position` - the position to insert the data into. if no position is specified the data is added to the beginning of the array.

`key => value` - a key/value pair for adding data to a hash.

## Returns

The data structure specified as the first argument

## Side Effects / Notes

- This function modifies the structure by adding new data to it.

## Examples

**Example:**
```sleep
@array = @("b", "c", "e", "f");

# insert d into the array
add(@array, "d", 2);

# insert a into the beginning of the array
add(@array, "a", 0);

println("@array is: " . @array);

```

**Output:**
```
@array is: @('a', 'b', 'c', 'd', 'e', 'f')

```

## See Also

[&addAll](addAll.md); [&remove](remove.md); [&removeAt](removeAt.md); [&removeAll](removeAll.md); [&splice](splice.md)
