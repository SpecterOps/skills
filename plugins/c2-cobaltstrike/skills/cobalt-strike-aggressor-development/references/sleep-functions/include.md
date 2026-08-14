# include

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/include.html

---

## Synopsis

```sleep
include(['/path/to/file.jar'], 'script.sl')
```

Compiles and executes the specified script in the current script context.

## Parameters

`'/path/to/file.jar'` - optionally a jar file that contains the script can be specified. If no .jar file is specified then the script will be loaded from the sleep.classpath value.

`'script.sl'` - this is the script to load and execute within the current script environment.

## Side Effects / Notes

- Loads and executes arbitrary sleep code.

- The scalar $__INCLUDE__ is set to the name of the included file. Included scripts may use this value to reference other resources relative to their location

## Errors

- Throws sleep.error.YourCodeSucksException if there are any errors within the included script.

- Throws [java.io.IOException](http://java.sun.com/javase/6/docs/api/java/io/IOException.md) if script can't be found

## Examples

**Example:**
```sleep
# foo.sl:
# sub foo {
# println("Hello World! Hello $name");
# }

include("foo.sl");
$name = "Horatio";
foo();

```

**Output:**
```
Hello World! Hello Horatio

```

## See Also

[&use](use.md)
