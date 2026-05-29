# getStackTrace

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/getStackTrace.html

---

## Synopsis

```sleep
@ getStackTrace()
```

Within the context of a catch block, this function will return a trace of the Sleep call stack that caused the caught exception condition to occur. Returns an empty array otherwise.

## Returns

An array of [sleep.runtime.ScriptInstance$SleepStackElement](../docs/api/sleep/runtime/ScriptInstance.SleepStackElement.md) objects. They have a decent String representation if you choose to utilize that.

## Side Effects / Notes

- Once this function is called, the stack trace will be cleared and subsequent calls will return an empty array.

## Examples

**Example:**
```sleep
sub bar
{
throw "I chose to do this :)";
}

sub foo
{
bar();
}

try
{
foo();
}
catch $exception
{
warn("Error is: $exception");
printAll(getStackTrace());
}

```

**Output:**
```
Warning: Error is: I chose to do this :) at getStackTrace.sl:17
getStackTrace.sl:13 &foo()
getStackTrace.sl:8 &bar()
getStackTrace.sl:3 <origin of exception>

```

## See Also

[&checkError](checkError.md); [&debug](debug.md); [&profile](profile.md); [&taint](taint.md); [&watch](watch.md); [&warn](warn.md)
