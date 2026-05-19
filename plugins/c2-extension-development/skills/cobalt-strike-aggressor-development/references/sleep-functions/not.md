# not

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/not.html

---

## Synopsis

```sleep
$ not(n)
```

Calculate the logical not value of the argument.

## Parameters

`n` - the value to apply this function to.

## Returns

A long scalar by default, unless the arg is an integer scalar then the return value is an integer scalar.

## Side Effects / Notes

- The rest of the Sleep logic operators include xor, left shift, right shift, etc. are all implemented as operators. Not exists as a function as Sleep does not have support for unary operators.

## Examples

**Example:**
```sleep
$flags = 0;

$flags = 2 | 64 | 128; # set some flags
println("1: " . formatNumber($flags, 2));

$flags = $flags & not(64); # unflag the 64 bit
println("2: " . formatNumber($flags, 2));

```

**Output:**
```
1: 11000010
2: 10000010

```
