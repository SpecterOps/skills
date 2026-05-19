# pushl

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/pushl.html

---

## Synopsis

```sleep
pushl([$var => value, ...])
```

creates an additional local scope.

## Parameters

`[$var => $value, ...]` - the local scope may be initialized with these key/value pairs.

## Side Effects / Notes

- Creates a new local scope. Be sure to use [&popl](popl.md) to destroy this local scope as Sleep will not do it for you.

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

[&popl](popl.md)
