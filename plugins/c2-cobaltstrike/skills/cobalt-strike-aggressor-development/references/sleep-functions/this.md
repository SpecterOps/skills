# this

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/this.html

---

## Synopsis

```sleep
this('$x $y')
```

Parses the specified string and declares all variables in the string as variables specific to the scope of the current closure.

## Parameters

`'$x $y'` - a string containing variable names separated by spaces.

## Side Effects / Notes

- Places specified variables into the this scope of the currently executing closure. Variables in the this scope persist between calls. These variables all start out with a value of $null.

## Examples

**Example:**
```sleep
global('$x');

sub foo {
this('$x');
$x = $x + 1;
println("&foo: \$x is $x");
}

$x = "bar!";
foo();
println("global: \$x is $x");
foo();
foo();

```

**Output:**
```
&foo: $x is 1
global: $x is bar!
&foo: $x is 2
&foo: $x is 3

```

## See Also

[&global](global.md); &local
