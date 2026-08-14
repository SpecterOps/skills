# ismatch

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/ismatch.html

---

## Synopsis

```sleep
"string" ismatch 'pattern'
```

Determine if the string matches the specified pattern.

## Parameters

`"string"` - the string to check

`'pattern'` - a regular expression pattern that defines a substring to match for

- 6. Regular Epxressions - tutorial on regular expression language

## Side Effects / Notes

- Text captured from the pattern is stored and made available via the [&matched](matched.md) function.

## Examples

**Example:**
```sleep
if ("(654) 555-1212" ismatch '\((\d\d\d)\) (\d\d\d-\d\d\d\d)')
{
($areaCode, $phoneNumber) = matched();
println("dial 1 and $areaCode before $phoneNumber");
}

```

**Output:**
```
dial 1 and 654 before 555-1212

```

## See Also

[&find](find.md); [hasmatch](hasmatch.md); [&join](join.md); [&matched](matched.md); [&matches](matches.md); [&replace](replace.md); [&split](split.md)
