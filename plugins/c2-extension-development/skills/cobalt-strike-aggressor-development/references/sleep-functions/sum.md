# sum

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/sum.html

---

## Synopsis

```sleep
$ sum(@|&, ...)
```

Calculates the product of corresponding array elements and returns the sum of these products.

## Parameters

`@|&` - the array to iterate through. The sum function loops based on the number of items in this array.

`...` - you may specifiy as many arrays as you like. If a subsequent array is shorter than the first, then the value 0.0 is used as a default.

## Returns

A double scalar containing the sum of all corresponding array element products.

## Examples

**Example:**
```sleep
# calculate weighted mean of the values
@values = @(90, 80, 82, 81);
@weights = @(20, 30, 25, 27);

println(sum(@values, @weights) / sum(@weights));

```

**Output:**
```
82.7156862745098

```
