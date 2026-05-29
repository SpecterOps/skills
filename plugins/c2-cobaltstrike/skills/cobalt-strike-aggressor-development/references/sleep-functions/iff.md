# iff

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/iff.html

---

## Synopsis

```sleep
$ iff(comparison, [$iftrue], [$iffalse])
```

Takes a comparison as the first parameter and returns it's second parameter if and only if the condition is true. The third parameter is returned if and only if the condition is false.

## Parameters

`comparison` - a condition to check for i.e. `$x > 0`

`$iftrue` - a value to return if the comparison evaluates to true. defaults to scalar integer 1.

`$iffalse` - a value to return if the comparison evaluates to false. defaults to $null

## Returns

$iftrue or $iffalse depending on the evaluation of comparison

## Side Effects / Notes

- This operator short circuits evaluation of its arguments. Only one of $iffalse or $iftrue will be evaluated depending on the outcome of the comparison.

- This function is a special case in the Sleep compiler. Normally it is not possible to use comparisons in an expression context.

## Examples

**Example:**
```sleep
sub foo
{
println("foo called!");
return "foo!";
}

sub bar
{
println("bar called!");
return "bar!";
}

$value = iff("a" eq "b", foo(), bar());
println($value);

```

**Output:**
```
bar called!
bar!

```
