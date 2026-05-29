# scalar

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/scalar.html

---

## Synopsis

```sleep
$ scalar($object)
```

Runs the specified object through the Java type to Sleep scalar conversion process. This same process used by HOES.

## Parameters

`$object` - an object scalar

## Returns

A scalar (of some sort)

## Examples

**Example:**
```sleep
println("Pre Conversion---");

$bytes = cast("this is a string", "b");
println("Class: " . [$bytes getClass]);
println("Type: " . typeOf($bytes));

println("Post Conversion---");

$value = scalar($bytes);
println("Class: " . [$value getClass]);
println("Type: " . typeOf($value));

```

**Output:**
```
Pre Conversion---
Class: class [B
Type: class sleep.engine.types.ObjectValue
Post Conversion---
Class: class java.lang.String
Type: class sleep.engine.types.StringValue

```

## See Also

[&newInstance](newInstance.md)
