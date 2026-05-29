# split

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/split.html

---

## Synopsis

```sleep
@ split('pattern', "string", [limit])
```

splits the specified string by the specified pattern

## Parameters

`"string"` - the string to split

`'pattern'` - the pattern that defines substrings this string should be broken up by.

- [6. Regular Epxressions](regex.md) - tutorial on regular expression language

`limit` - limits the number of segments to split the sentence into.

## Returns

a scalar array

## Examples

**Example:**
```sleep
@data = @("Raphael,Professional Escort,NY",
"Frances,Sales Warrior,MI");

foreach $var (@data)
{
($name, $job, $state) = split(',', $var);
println("$name works as a $job in $state");
}

```

**Output:**
```
Raphael works as a Professional Escort in NY
Frances works as a Sales Warrior in MI

```

## See Also

[&find](find.md); [hasmatch](hasmatch.md); [ismatch](ismatch.md); [&join](join.md); [&matched](matched.md); [&matches](matches.md); [&replace](replace.md)
