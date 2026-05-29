# values

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/values.html

---

## Synopsis

```sleep
@ values(%hash, [@|&keys])
```

Generates an array containing the values within the specified hash.

## Parameters

`%hash` - the hash to extract the values from.

`@|&keys` - specifies which keys to extract from the hash.

## Returns

An array with copies/references to all the values from the specified hash.

## Examples

**Example:**
```sleep
%data = %(a => "AT-ST Walker", b => "bat", c => "cat", d => 43);

foreach $var (values(%data))
{
println($var);
}

```

**Output:**
```
43
AT-ST Walker
cat
bat

```

## See Also

[&keys](keys.md); [&size](size.md)
