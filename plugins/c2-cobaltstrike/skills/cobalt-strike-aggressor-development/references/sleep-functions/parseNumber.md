# parseNumber

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/parseNumber.html

---

## Synopsis

```sleep
$ parseNumber("number", [base])
```

Parses the specified number string using the specified base system.

## Parameters

`"number"` - the string to parse.

`base` - an integer indicating the base to use, defaults to 10. The following table contains a few options, really this function is flexible towards any base system you choose to specify.

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
$value = parseNumber("1337", 16);
println("0x1337 is: $value");

$value = parseNumber("10001001", 2);
println("10001001 is: $value");

```

**Output:**
```
0x1337 is: 4919
10001001 is: 137

```

## See Also

[&formatNumber](formatNumber.md)
