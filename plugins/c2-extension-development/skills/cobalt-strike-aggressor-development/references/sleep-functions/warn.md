# warn

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/warn.html

---

## Synopsis

```sleep
warn("text")
```

Prints "text" to the registered runtime warning watcher. Provides an application neutral way to print messages to the Sleep console.

## Parameters

`"text"` - the text to write

## Examples

**Example:**
```sleep
try
{
$handle = openf("doesNotExist");
throw checkError($error);

println("file opened!");
}
catch $exception
{
warn("error: $exception");
}

```

**Output:**
```
Warning: error: java.io.FileNotFoundException: /Users/raffi/manual/manual/doesNotExist (No such file or directory) at choice1.sl:10

```

## See Also

[&checkError](checkError.md); [&debug](debug.md); [&getStackTrace](getStackTrace.md); [&profile](profile.md); [&taint](taint.md); [&watch](watch.md)
