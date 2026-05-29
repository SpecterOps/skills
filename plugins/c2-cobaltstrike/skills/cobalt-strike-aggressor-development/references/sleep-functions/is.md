# is

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/is.html

---

## Synopsis

```sleep
? $a is $b
```

Determine if $a references the same data as $b

## Parameters

`$a` - any scalar

`$b` - any scalar

## Examples

**Output:**
```
$ java -jar sleep.jar
>> Welcome to the Sleep scripting language
> ? $null is ""
false
> ? $null is 0
false
> ? $null is $null
true

```

## See Also

[isa](isa.md); [&typeOf](typeOf.md)
