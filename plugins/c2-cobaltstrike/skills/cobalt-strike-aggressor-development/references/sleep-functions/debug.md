# debug

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/debug.html

---

## Synopsis

```sleep
$ debug([level])
```

query/set the debug level for the current script environment.

## Parameters

`level` - an integer specifying the current debug level. Debug levels can be OR'd together.
The following debug levels can be combined with the OR operator i.e. `1 | 24`:

LevelDescription
1display all hard errors as runtime warnings.
2display all soft errors as runtime warnings. These are the same errors that are caught programatically using [&checkError](checkError.md)
4display a runtime warning for the first time use of non-declared variables.
8trace all function calls (collects profiler statistics)
24trace function calls only for the purpose of collecting profiler statistics
34"throw" all errors flagged for use with [&checkError](checkError.md)
64trace all predicate decisions (follow program logic)
128trace propagation of tainted values

If no argument is specified then the current debug level is returned with no changes.

## Returns

the current debug level

## Examples

**Example:**
```sleep
# query and print the current debug level

$level = debug();
println("The current debug level is $level");

# turn off all debug warnings

debug(0);

# enable all debug warnings

debug(7);

# enable debug options 1 and 4

debug(1 | 4);

# turn on debug option 4 (without affecting other options)

debug(debug() | 4);

# turn off debug option 4 (without affecting other options)

debug(debug() & not(4));

```

**Output:**
```
The current debug level is 1

```

## See Also

[&checkError](checkError.md); [&getStackTrace](getStackTrace.md); [&profile](profile.md); [&taint](taint.md); [&watch](watch.md); [&warn](warn.md)
