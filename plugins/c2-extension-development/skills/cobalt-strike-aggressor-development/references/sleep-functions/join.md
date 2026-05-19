# join

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/join.html

---

## Synopsis

```sleep
$ join("string", @array|&closure)
```

joins the elements of @array with "string"

## Parameters

`"string"` - the delimeter to join the elements together with.

`@array` - an array of elements to join together

`&closure` - a generator function to create elements to join with the specified string

## Returns

a scalar string

## Examples

**Example:**
```sleep
$string = join(', ', @("ape", "bat", "cat", "dog"));
println($string);

```

**Output:**
```
ape, bat, cat, dog

```

## See Also

[&find](find.md); [hasmatch](hasmatch.md); [ismatch](ismatch.md); [&matched](matched.md); [&matches](matches.md); [&replace](replace.md); [&split](split.md)
