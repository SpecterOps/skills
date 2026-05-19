# spaceship

**Category:** Math

**Source:** https://sleep.dashnine.org/manual/spaceship.html

---

## Synopsis

```sleep
$a <=> $b
```

performs a numerical comparison of $a and $b

## Parameters

`$a` - any scalar, converted to a double

`$b` - any scalar, converted to a double

## Returns

A value based on comparing $a and $b

ValueDescription
0$a is equal to $b
< 0$a is less than $b
> 0$a is greater than $b

## Examples

**Example:**
```sleep
sub reverseNumericalOrder
{
return $2 <=> $1;
}

@array = @(3, 10, 99, 4.5, 8, 7.534535636, 2, 0.01);
@sorted = sort(&reverseNumericalOrder, @array);

println(@sorted);

```

**Output:**
```
@(99, 10, 8, 7.534535636, 4.5, 3, 2, 0.01)

```

## See Also

[<=>](spaceship.md); [cmp](cmp.md); [&sort](sort.md); [&sorta](sorta.md); [&sortd](sortd.md); [&sortn](sortn.md)
