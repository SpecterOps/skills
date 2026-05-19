# find

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/find.html

---

## Synopsis

```sleep
$ find("string", 'pattern', [start])
```

Returns the index of the first substring that matches 'pattern' starting from the specified index.

## Parameters

`"string"` - the string to search.

`'pattern'` - a pattern describing the substring to search for.

- [6. Regular Epxressions](regex.md) - tutorial on regular expression language

`start` - the position from which to begin the search (default is 0)

## Returns

A scalar integer with the index. A failed search will return $null.

## Examples

**Example:**
```sleep
# very naive sentence parser with &find

sub parseSentence
{
$start = 0;
while $index (find($1, '(([?!.])\s*)', $start))
{
($match, $type) = matched();

if ($type eq "?")
{
println("Question: " . substr($1, $start, $index));
}
else if ($type eq "!")
{
println("Excitement: " . substr($1, $start, $index));
}
else
{
println("Boring: " . substr($1, $start, $index));
}

$start = $index + strlen($match);
}
}

parseSentence("This is a sentence! And so is this. Questions? Nope.");

```

**Output:**
```
Excitement: This is a sentence
Boring: And so is this
Question: Questions
Boring: Nope

```

## See Also

[hasmatch](hasmatch.md); [ismatch](ismatch.md); [&join](join.md); [&matched](matched.md); [&matches](matches.md); [&replace](replace.md); [&split](split.md)
