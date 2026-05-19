# size

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/size.html

---

## Synopsis

```sleep
$ size(@array)
```

return the number of elements in @array.

```sleep
$ size(%hash)
```

return the number of elements in %hash.

## Parameters

`@array, %hash` - the data structure to get the number of elements from

## Side Effects / Notes

- `size(%hash)` executes in O(n) time. This is because it loops through the hash and keys associated with $null. If you'd like to avoid this behavior use `[[%hash getData] size` instead.

## Examples

**Example:**
```sleep
@a = @("a", "b", "c", "d", "e");
$size = size(@a);

println($size);

```

**Output:**
```
5

```
