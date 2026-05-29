# exit

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/exit.html

---

## Synopsis

```sleep
exit(["reason"])
```

Causes the currently executing script to stop executing.

## Parameters

`"reason"` - an optional parameter, when a reason is specified, this will be printed as a runtime warning.

## Side Effects / Notes

- Discards the current call stack. The exit function works by throwing an uncatchable exception within the Sleep interpreter. This exception causes execution to stop.

## Examples

**Example:**
```sleep
debug(15); # 15 is for trace...

sub fact {
if ($1 == 0) {
exit("I just feel like it!");
}
return $1 * fact($1 - 1);
}

fact(2);

```

**Output:**
```
Trace: &exit('I just feel like it!') - FAILED! at exit.sl:5
Warning: I just feel like it! at exit.sl:5
Trace: &fact(0) - FAILED! at exit.sl:7
Trace: &fact(1) - FAILED! at exit.sl:7
Trace: &fact(2) - FAILED! at exit.sl:10

```
