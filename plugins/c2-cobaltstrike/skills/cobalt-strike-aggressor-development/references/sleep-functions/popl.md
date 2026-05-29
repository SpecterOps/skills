# popl

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/popl.html

---

## Synopsis

```sleep
popl([$var => value, ...])
```

removes current local scope restoring previous scope.

## Parameters

`[$var => $value, ...]` - the restored local scope may be updated with these key/value pairs taken from the current scope.

## Side Effects / Notes

- Pops the current local scope. Be sure the current scope was created with [&pushl](pushl.md) or else bad things will happen.

## Examples

**Example:**
```sleep
inline swap
{
pushl($a => $1, $b => $2);

local('$temp');
$temp = $b;
$b = $a;
$a = $temp;

popl();
}

sub bar
{
local('$x $y $temp');
$temp = 100;
$x = 3;
$y = 9;
println("\$x: $x and \$y: $y");
swap($x, $y);
println("\$x: $x and \$y: $y (and $temp $+ )");
}

bar();

```

**Output:**
```
$x: 3 and $y: 9
$x: 9 and $y: 3 (and 100)

```

## See Also

[&pushl](pushl.md)
