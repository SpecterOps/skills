# rand

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/rand.html

---

## Synopsis

```sleep
$ rand([number])
```

generates a random integer between 0 and number. If number is ommited the function generates a random double between 0 and 1

```sleep
$ rand(@array)
```

returns a random element of @array

## Parameters

`number` - returns a number between 0 and number if a number is specified. If no number is specified a random double value between 0 and 1 is returned.

`@array` - if the parameter is an array, a random element of the array is returned.

## Returns

depends on the first parameter.

## Examples

**Example:**
```sleep
# print a random number between 0 and 10.
println("Random Number: " . rand(10));

# print a random array element
@array = @("a", "b", "c", "d", "e", "f", "g");
println("Element: " . rand(@array));

# get a random double between 0 and 1.0
println(rand());

```

**Output:**
```
Random Number: 4
Element: d
0.26217141921515497

```

## See Also

[&srand](srand.md)
