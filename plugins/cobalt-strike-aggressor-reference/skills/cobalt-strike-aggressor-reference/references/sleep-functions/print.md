# print

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/print.html

---

## Synopsis

```sleep
print([$handle], "text")
```

prints "text" to the specified handle (with no newline)

## Parameters

`$handle` - the handle to write to (defaults to stdin/stdout)

`"text"` - the data to write

## Examples

**Example:**
```sleep
print("A spoon");
print(" full of");
print(" sugar...");
println(" helps the medicine go down");

```

**Output:**
```
A spoon full of sugar... helps the medicine go down

```

## See Also

[&bwrite](bwrite.md); [&printAll](printAll.md); [&println](println.md); [&writeb](writeb.md); [&writeObject](writeObject.md)
