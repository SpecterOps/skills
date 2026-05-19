# log

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/log.html

---

## Synopsis

```sleep
$ log(n, [base])
```

Calculate the logarithm of the specified argument.

## Parameters

`n` - the value (converted to a double) to apply this function to.

`base` - the base to use, if no base is specified, then the natural logarithm of n is calculated.

## Returns

A double scalar.

## Examples

**Example:**
```sleep
sub log10
{
return log($1) / log(10);
}

println("log10(2): " . log10(2));
println("log10(3): " . log10(3));
println("log10(5): " . log10(5));

```

**Output:**
```
log10(2): 0.30102999566398114
log10(3): 0.4771212547196623
log10(5): 0.6989700043360187

```

## See Also

[&exp](exp.md); [&sqrt](sqrt.md)
