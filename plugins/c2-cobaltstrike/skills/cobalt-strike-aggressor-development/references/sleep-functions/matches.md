# matches

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/matches.html

---

## Synopsis

```sleep
@ matches("string", 'pattern', [n], [m])
```

returns the matches from "string" applied to the regex 'pattern'. if n is specified this will return the grouped matches of the n'th substring matching the specified pattern. if n and m are specified, all of the grouped matches of the n-m substrings will be returned.

## Parameters

`"string"` - the string to match against the pattern and extract substrings from

`'pattern'` - a regular expression pattern that defines wether or not we have a match

- 6. Regular Epxressions - tutorial on regular expression language

## Examples

**Example:**
```sleep
# trim whitespace from start of a string
$trimmed = matches("\t this is a test", '\s*(.*)')[0];
println($trimmed);

```

**Output:**
```
this is a test

```

## See Also

[&find](find.md); [hasmatch](hasmatch.md); [ismatch](ismatch.md); [&join](join.md); [&matched](matched.md); [&replace](replace.md); [&split](split.md)
