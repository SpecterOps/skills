# casti

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/casti.html

---

## Synopsis

```sleep
$ casti($scalar, 't')
```

casts an individual $scalar into an object scalar representing a Java value

## Parameters

`$scalar` - the scalar to cast into a Java value

`'t'` - the type to cast to

CharacterDescription
bbyte
cchar
ddouble

ffloat
hshort
iint
llong
zboolean

ojava.lang.Object
*Java Object (determined by class of scalars object value)

You may also specify a `^Class` literal to cast to something specific.

## Returns

A sleep scalar with a reference to a Java value of the specified type.

## Examples

**Example:**
```sleep
$cast = casti(1, 'b');
println([$cast getClass]);

$cast = casti(33.5, 'f');
println([$cast getClass]);

```

**Output:**
```
class java.lang.Byte
class java.lang.Float

```

## See Also

[&cast](cast.md); [&double](double.md); [&int](int.md); [&long](long.md); [&uint](uint.md)
