# replace

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/replace.html

---

## Synopsis

```sleep
$ replace("string", 'pattern', "new", [n])
```

Replaces each substring of the specified string that matches the regular expression pattern with the specified new string.

## Parameters

`"string"` - the string to replace text in.

`'pattern'` - a regular expression pattern defining a substring that should be replaced.

- [6. Regular Epxressions](regex.md) - tutorial on regular expression language

`"new"` - the new text to replace each occurence of the pattern with. Within this string the literals $1, $2, etc. will be expanded to the pattern groupings captured by the pattern matcher. These are not Sleep variables, rather they are a special sequence interpreted by the regex engine.

`n` - if specified, only n occurences will be replaced. The default is to replace all matching substrings.

## Returns

a scalar string

## Examples

**Example:**
```sleep
$string = replace("foo is the word, not bar!", '\Afoo|\Abar', "pHEAR");
println($string);

```

**Output:**
```
pHEAR is the word, not bar!

```

## See Also

[&find](find.md); [hasmatch](hasmatch.md); [ismatch](ismatch.md); [&join](join.md); [&matched](matched.md); [&matches](matches.md); [&split](split.md)
