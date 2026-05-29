# reverse

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/reverse.html

---

## Synopsis

```sleep
@ reverse(@|&)
```

Returns a copy of the specified array/iterator in reverse order.

## Parameters

`@|&` - the array or iterator to copy and reverse.

## Returns

A copy of the specified array or iterator in reverse order.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", 1, 2, 3.0);
@copy = reverse(@array);

println(@copy);

```

**Output:**
```
@(3.0, 2, 1, 'c', 'b', 'a')

```

**Example:**
```sleep
sub iterator
{
local('$x');
for ($x = 0; $x < 4; $x++)
{
yield $x * 45;
}
}

@copy = reverse(&iterator);
println(@copy);

```

**Output:**
```
@(135, 90, 45, 0)

```

## See Also

[&clear](clear.md); [&concat](concat.md); [&flatten](flatten.md); [&sublist](sublist.md); [&splice](splice.md)
