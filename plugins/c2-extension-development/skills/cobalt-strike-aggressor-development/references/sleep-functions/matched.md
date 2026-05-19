# matched

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/matched.html

---

## Synopsis

```sleep
@ matched()
```

returns the matches from a "string" applied to a regex 'pattern' during an [ismatch](ismatch.md)/[hasmatch](hasmatch.md) check

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

[&find](find.md); [hasmatch](hasmatch.md); [ismatch](ismatch.md); [&join](join.md); [&matches](matches.md); [&replace](replace.md); [&split](split.md)
