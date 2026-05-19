# taint

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/taint.html

---

## Synopsis

```sleep
$ taint($scalar)
```

Taints the specified scalar

## Parameters

`$scalar` - the scalar to taint

## Returns

The passed in scalar.

## Side Effects / Notes

- The scalar is modified directly.

## Examples

**Example:**
```sleep
debug(debug() | 128);

$script = 'println(' . @ARGV[0] . ');';
eval($script);

```

**Output:**
```
$ java -jar sleep.jar taint.sl "2 + 2"
4
$ java -Dsleep.taint=true -jar sleep.jar taint.sl "2 + 2"
Warning: tainted value: '2 + 2);' from: '2 + 2' at taint.sl:3
Warning: tainted value: 'println(2 + 2);' from: '2 + 2);' at taint.sl:3
Warning: Insecure &eval: 'println(2 + 2);' is tainted at taint.sl:4

```

## See Also

[-istainted](pr_istainted.md); [&untaint](untaint.md)
