# checkError

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/checkError.html

---

## Synopsis

```sleep
$ checkError([$error])
```

Returns the last error message to occur.

## Parameters

`$error` - a scalar to place the last error object into. Often times this error object will be an instance of a [java.lang.Exception](http://java.sun.com/javase/6/docs/api/java/lang/Exception.md).

## Returns

The last error object. The same one placed into the $error parameter.

## Side Effects / Notes

- Clears the error condition so subsequent calls to [&checkError](checkError.md) will result in $null.

- The value of the $error scalar is updated with the last error object. ala Perl's $!

- This is but one error handling mechanism available, a more Java-style try/catch can be forced with debug level 34. This debug level will cause the error message to be thrown any time an error is flagged.

- Debug level 2 will automatically print out a notification any time a checkError value is flagged.

## Examples

**Example:**
```sleep
$handle = openf(">/etc/shadow");

if (checkError($error))
{
warn("Could not open the file: $error");
}

```

**Output:**
```
Warning: Could not open the file: java.io.FileNotFoundException: /etc/shadow (Permission denied) at checkError.sl:5

```

## See Also

[&debug](debug.md); [&getStackTrace](getStackTrace.md); [&profile](profile.md); [&taint](taint.md); [&watch](watch.md); [&warn](warn.md)
