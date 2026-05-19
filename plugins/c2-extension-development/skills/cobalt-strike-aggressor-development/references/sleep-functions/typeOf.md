# typeOf

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/typeOf.html

---

## Synopsis

```sleep
^ typeOf($scalar)
```

Returns the Java class of the container referenced by $scalar

## Parameters

`$scalar` - The scalar to return the type of

## Returns

A Java class object.

## Examples

**Example:**
```sleep
$long = 4L;
$double = 3.5;

$result = $long + $double; # what is the result?

println("Type of result is: " . typeOf($result));

```

**Output:**
```
Type of result is: class sleep.engine.types.DoubleValue

```

## See Also

[is](is.md); [isa](isa.md)
