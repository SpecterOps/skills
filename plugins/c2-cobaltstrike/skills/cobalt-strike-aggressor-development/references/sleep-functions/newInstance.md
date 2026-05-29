# newInstance

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/newInstance.html

---

## Synopsis

```sleep
$ newInstance(^Class|@array, &closure)
```

Creates an instance of the specified Java interface (or interfaces if an array is used) backed by the specified closure.

## Parameters

`^Class` - the class to create an instance of (limited to Java interfaces for now)

`@array` - an array of Java classes to create an instance of

`&closure` - the closure to back this proxy Java object with.

## Returns

an instance of a Java object that implements the specified interfaces.

## Side Effects / Notes

- Calls to this Java object will be passed on to the specified closure. $0 is the method name and $1, $2, ... are the arguments to the method. The closure is responsible for returning the right Java type.

## Examples

**Example:**
```sleep
@list = @("a", "b", "c", "d", "e");

sub iterator
{
if ($0 eq "hasNext")
{
return size(@data);
}

if ($0 eq "next")
{
return shift(@data);
}
}

$iter = newInstance(^java.util.Iterator, lambda(&iterator, @data => @list));

while ([$iter hasNext])
{
$element = [$iter next];
println($element);
}

```

**Output:**
```
a
b
c
d
e

```

## See Also

[&scalar](scalar.md)
