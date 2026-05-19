# degrees

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/degrees.html

---

## Synopsis

```sleep
$ degrees(n)
```

Converts the angle n measured in radians to an approximately equivalent angle in degrees.

## Parameters

`n` - the value (converted to a double) to apply this function to.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
$convert = degrees([Math PI] * 4);
println("4 / Pi radians is $convert degrees");

$convert = degrees([Math PI] * 0.25);
println("4 Pi (.025 / Pi) radians is $convert degrees");

```

**Output:**
```
4 / Pi radians is 720.0 degrees
4 Pi (.025 / Pi) radians is 45.0 degrees

```

## See Also

[&radians](radians.md)
