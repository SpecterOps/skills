# setField

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/setField.html

---

## Synopsis

```sleep
setField(^Class|$object, field => value, ...)
```

Sets any number of public/protected fields of the specified class or instance of $object to their corresponding values.

## Parameters

`^Class` - a literal of the class to set a static field for.

`$object` - an instance of a class to set a field for.

`field => value` - an arbitrary field name followed by a corresponding value which is converted to the type Java expects.

`...` - the field => value parameter can be repeated any number of times with more values to set.

## Side Effects / Notes

- Updates the members of the specified class or instance.

## Errors

- An error is thrown if the field as named does not exist.

- An error is thrown if the specified value can not be converted to the Java type.

## Examples

**Example:**
```sleep
import java.awt.Point;

$p = [new Point];
setField($p, x => 33, y => 45);
println($p);

```

**Output:**
```
java.awt.Point[x=33,y=45]

```
