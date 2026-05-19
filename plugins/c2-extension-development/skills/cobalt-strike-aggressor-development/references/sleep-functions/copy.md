# copy

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/copy.html

---

## Synopsis

```sleep
@ copy(@array)
```

Returns a shallow copy of the specified array.

```sleep
$ copy($scalar)
```

Returns a shallow copy of the specified scalar.

```sleep
% copy(%hash)
```

Returns a shallow copy of the specified hash.

## Parameters

`@array|$scalar|%hash` - the data to copy.

## Returns

A shallow copy of the specified data type.

## Examples

**Example:**
```sleep
@a = @(1, 2, 3, 4, 5);
@b = copy(@a);

@a[2] = "moo";

println("@a is now: " . @a);
println("@b is now: " . @b);

```

**Output:**
```
@a is now: @(1, 2, 'moo', 4, 5)
@b is now: @(1, 2, 3, 4, 5)

```

## See Also

[&add](add.md); [&addAll](addAll.md); [&remove](remove.md); [&removeAt](removeAt.md); [&removeAll](removeAll.md); [&splice](splice.md)
