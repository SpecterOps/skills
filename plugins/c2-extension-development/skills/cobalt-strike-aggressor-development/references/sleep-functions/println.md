# println

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/println.html

---

## Synopsis

```sleep
println([$handle], "text")
```

prints "text" to the specified handle (with a newline appended)

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`"text"` - the text to write

## Examples

**Example:**
```sleep
println("Hello World");

```

**Output:**
```
Hello World

```

## See Also

[&bwrite](bwrite.md); [&print](print.md); [&printAll](printAll.md); [&writeb](writeb.md); [&writeObject](writeObject.md)
