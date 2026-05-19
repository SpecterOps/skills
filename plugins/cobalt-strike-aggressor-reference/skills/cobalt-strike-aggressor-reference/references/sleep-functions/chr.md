# chr

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/chr.html

---

## Synopsis

```sleep
$ chr(n)
```

Returns a string containing the character that corresponds to the integer argument.

## Parameters

`n` - the ascii integer value

## Returns

A scalar string.

## Examples

**Example:**
```sleep
for ($x = 65; $x < 91; $x++)
{
print(chr($x));
}
println();

```

**Output:**
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ

```

## See Also

[&asc](asc.md)
