# untaint

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/untaint.html

---

## Synopsis

```sleep
$ untaint($scalar)
```

Untaints the specified scalar

## Parameters

`$scalar` - the scalar to untaint

## Returns

The passed in scalar.

## Side Effects / Notes

- The scalar is modified directly.

## Examples

**Example:**
```sleep
# makes user input safe for use within a regex pattern
# we use inline because all function return values are considered
# tainted if an arg is tainted. inline allows us to abstract our
# operation on the argument and untaint the value.
inline quote_regex
{
untaint($1);
$1 = "\\Q $+ $1 $+ \\E";
}

println("before: " . iff(-istainted @ARGV[0], "tainted!", "not tainted"));
quote_regex(@ARGV[0]);

println("after: " . iff(-istainted @ARGV[0], "tainted!", "not tainted"));
println(@ARGV[0]);

```

**Output:**
```
$ java -Dsleep.taint=true -jar sleep.jar untaint.sl ".*?"
before: tainted!
after: not tainted
\Q.*?\E

```

## See Also

[-istainted](pr_istainted.md); [&taint](taint.md)
