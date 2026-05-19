# printAll

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/printAll.html

---

## Synopsis

```sleep
printAll([$handle], @array|&generator)
```

prints entire contents of passed in @array or &generator to $handle. each element has a newline appended to it.

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`@array` - an array containing lines of text to be printed out

`&generator` - a function that generates lines of text to be printed out. $null stops the generator.

## Examples

**Example:**
```sleep
@array = @("Jill", "Jack", "BoB", "iReNE", "aDaWG");

sub my_sort
{
return lc($1) cmp lc($2);
}

sort(&my_sort, @array);

printAll(@array);

```

**Output:**
```
aDaWG
BoB
iReNE
Jack
Jill

```

## See Also

[&bwrite](bwrite.md); [&print](print.md); [&println](println.md); [&writeb](writeb.md); [&writeObject](writeObject.md)
