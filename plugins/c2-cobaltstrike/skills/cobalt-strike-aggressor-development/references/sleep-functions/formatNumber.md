# formatNumber

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/formatNumber.html

---

## Synopsis

```sleep
$ formatNumber(number, [from], to)
```

Parses the specified number string using the specified base system.

## Parameters

`number` - our number to format from one base system to another.

`from` - the base system to interpret the number with. (default is 10)

`to` - the base system to format the number into, default is 10. The following table contains a few options, really this function is flexible towards any base system you choose to specify.

BaseDescription
2binary
8octal
10decimal
16hex

## Returns

A long scalar resulting from parsing the number string with the specified base.

## Examples

**Example:**
```sleep
$value = formatNumber(4919, 16);
println("4919 is: 0x $+ $value");

$value = formatNumber(137, 2);
println("137 is: $value");

```

**Output:**
```
4919 is: 0x1337
137 is: 10001001

```

## See Also

[&parseNumber](parseNumber.md)
