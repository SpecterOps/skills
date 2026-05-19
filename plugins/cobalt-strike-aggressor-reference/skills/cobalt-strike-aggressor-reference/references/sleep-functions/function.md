# function

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/function.html

---

## Synopsis

```sleep
& function('&name')
```

Obtains a reference to the specified function.

## Parameters

`'&name'` - the name of the function to obtain the handle for.

## Returns

$null if the function doesn't exit or a scalar containing the function object.

## Examples

**Example:**
```sleep
sub foo {
println("foo function w/ $1");
}

foo("new color protection");

$func = function('&foo');
[$func: "cool spikes"];

```

**Output:**
```
foo function w/ new color protection
foo function w/ cool spikes

```

## See Also

[&inline](inline.md); [&invoke](invoke.md); [&setf](setf.md)
