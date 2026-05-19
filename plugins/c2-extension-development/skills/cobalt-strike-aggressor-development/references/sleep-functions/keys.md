# keys

**Category:** Hashes

**Source:** https://sleep.dashnine.org/manual/keys.html

---

## Synopsis

```sleep
@ keys(%hash)
```

Generates an array containing the keys within the specified hash.

## Parameters

`%hash` - the hash to extract the keys from.

## Returns

An array with copies of all the keys from the specified hash.

## Examples

**Example:**
```sleep
%data = %(a => "AT-ST Walker", b => "bat", c => "cat", d => 43);

foreach $var (keys(%data))
{
println($var);
}

```

**Output:**
```
d
a
c
b

```

## See Also

[&size](size.md); [&values](values.md)
