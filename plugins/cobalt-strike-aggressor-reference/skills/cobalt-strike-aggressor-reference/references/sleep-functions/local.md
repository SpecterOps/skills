# local

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/local.html

---

## Synopsis

```sleep
local('$x $y')
```

Parses the specified string and declares all variables in the string as local variables.

## Parameters

`'$x $y'` - a string containing variable names separated by spaces.

## Side Effects / Notes

- Places specified variables into the local scope of the currently executing function. These variables all start out with a value of $null.

## Examples

**Example:**
```sleep
global('$x');

sub foo {
local('$x');
$x = "foo!";
println("&foo: \$x is $x");
}

$x = "bar!";
foo();
println("global: \$x is $x");

```

**Output:**
```
&foo: $x is foo!
global: $x is bar!

```

## See Also

[&global](global.md); [&this](this.md)
