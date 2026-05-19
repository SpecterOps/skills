# isa

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/isa.html

---

## Synopsis

```sleep
? $a isa ^Class
```

Determine if object value of $a is an instance of the specified `^Class`

## Parameters

`$a` - any scalar

`^Class` - a class to check.

## Examples

**Output:**
```
>> Welcome to the Sleep scripting language
> ? "some string" isa ^String
true
> ? 33.0 isa ^String
false
> ? 33.0 isa ^Double
true

```

## See Also

[is](is.md); [&typeOf](typeOf.md)
