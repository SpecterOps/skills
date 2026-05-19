# cast

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/cast.html

---

## Synopsis

```sleep
$ cast(@array, 't', ...)
```

Casts @array into an object scalar representing a native java array.

```sleep
$ cast("string", 'b'|'c')
```

Casts the specified string of byte data into a 1-dimensional native java byte or character array

## Parameters

`@array` - the array to cast into a native java array. A copy of this array is flattened before conversion.

`"string"` - a string used to represent an array of bytes or characters

`'t'` - the type of this new native array

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

`...` - the dimensions of the native array. i.e. 2, 2 would mean a 2x2 array.

## Returns

A sleep scalar with a reference to a java array Object of the specified type and dimensions.

## Examples

**Example:**
```sleep
@array = @("a", "b", "c", "d", "e", "f");
$casted = cast(@array, "*", 2, 3); # create a 2x3 array

println("Class is: " . [$casted getClass]);

```

**Output:**
```
Class is: class [[Ljava.lang.String;

```

## See Also

[&casti](casti.md); [&double](double.md); [&int](int.md); [&long](long.md); [&uint](uint.md)
