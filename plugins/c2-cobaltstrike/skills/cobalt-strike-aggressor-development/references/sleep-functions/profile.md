# profile

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/profile.html

---

## Synopsis

```sleep
@ profile()
```

Returns the profiler statistics for the current script environment. Profiler statistics will only be collected if DEBUG_TRACE_CALLS (8) or DEBUG_TRACE_PROFILE_ONLY (24) are enabled.

## Returns

An array of [sleep.runtime.ScriptInstance$ProfilerStatistic](../docs/api/sleep/runtime/ScriptInstance.ProfilerStatistic.md) objects. They have a decent String representation if you choose to utilize that.

## Side Effects / Notes

- As mentioned in the synopsis, certain debug levels must be enabled for profiler statistics to be collected. These levels are enabled through the &debug function.

## Examples

**Example:**
```sleep
# enable collection of profiler statistics
debug(debug() | 24);

# some activity to give us something to profile...
sub fact {
return iff($1 == 0, 1, $1 * [$this : $1 - 1]);
}

$x = ["test" length];
[{ return "this is a closure call!: " . fact(10.0); }];

# print out the profile of this code...
@stats = profile();
foreach $var (@stats) {
println($var);
}

```

**Output:**
```
0.0010s 10 &closure[profile.sl:6]
0.0s 1 &fact
0.0s 1 public int java.lang.String.length()
0.0s 1 &closure[profile.sl:10]

```

## See Also

[&checkError](checkError.md); [&debug](debug.md); [&getStackTrace](getStackTrace.md); [&taint](taint.md); [&watch](watch.md); [&warn](warn.md)
