# cmp

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/cmp.html

---

## Synopsis

```sleep
$a cmp $b
```

performs an alphabetical comparison of $a and $b

## Parameters

`$a` - any scalar, converted to a string

`$b` - any scalar, converted to a string

## Returns

A value based on comparing $a and $b

ValueDescription
0$a is equal to $b
< 0$a is less than $b
> 0$a is greater than $b

## Examples

**Example:**
```sleep
sub caseInsensitiveCompare
{
$a = lc($1);
$b = lc($2);

return $a cmp $b;
}

@array = @("zebra", "Xanadu", "ZooP", "ArDvArKS", "Arks", "bATS");
@sorted = sort(&caseInsensitiveCompare, @array);

println(@sorted);

```

**Output:**
```
@('ArDvArKS', 'Arks', 'bATS', 'Xanadu', 'zebra', 'ZooP')

```

## See Also

[<=>](spaceship.md); [&sort](sort.md); [&sorta](sorta.md); [&sortd](sortd.md); [&sortn](sortn.md)
