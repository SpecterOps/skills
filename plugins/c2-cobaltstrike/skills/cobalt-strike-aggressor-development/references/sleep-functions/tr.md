# tr

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/tr.html

---

## Synopsis

```sleep
$ tr("string", "matcher", "replacement", ['options'])
```

A character translation utility similar to the UNIX tr command. A transliteration consists of a pattern of characters to match and a pattern, typically of equal length, of characters to replace each match with. The tr utility loops through a specified string character by character. Each character is compared against the pattern of matching characters. If the character matches one of the pattern characters it is either replaced with the replacement character mapped to that matcher or it is deleted. Which action is taken depends on what options are specified.

## Parameters

`"string"` - the string to apply this translation function to.

`"matcher"` - the characters that will be swapped out. Ranges will be expanded to all of the characters. A range is specified as n-m where n is the starting character (A-Z, a-z, 0-9) and m is the ending character. Backwards ranges are allowed as well. The matcher pattern may also contain the following character classes:

SequenceMeaning

.Matches any character
\dMatches any digit 0-9
\DMatches any non-digit
\sMatches any whitespace character
\SMatches any non-whitespace character
\wMatches any word character (a-z, A-Z, _, and 0-9)
\WMatches any non-word character
\\Matches a literal backslash
\.Matches a literal period
\-Matches a literal dash

`"replacement"` - a string of replacement characters that maps 1:1 (after expansion) to the "matcher" string. As with the "matcher" string, ranges are expanded here as well.

`'options'` - A combination of the following parameters that alters the behavior of the matcher/translator.

SequenceNameDescription
ccomplement negates matcher pattern forcing matcher chars/patterns to match their complement.
ddeletedelete all characters with no mapping in the replacement pattern.
ssqueezesqueeze together matches that occur next to eachother. Deletes repeated matches.

## Returns

The transliterated string.

## Examples

**Example:**
```sleep
# A simple ROT13 Translator (for extra security run it twice...)

$cipher = tr("sleep rocks", "a-z", "n-za-m");
$plain = tr($cipher, "a-z", "n-za-m");

println("Cipher: $cipher Plain: $plain");

```

**Output:**
```
Cipher: fyrrc ebpxf Plain: sleep rocks

```

**Example:**
```sleep
# remove all duplicate chars from $string

$string = "thhisss iiiisss mmmy sssstrriinngg";
$string = tr($string, "a-zA-Z0-9 ", "a-zA-Z0-9 ", "sd");

println($string);

```

**Output:**
```
this is my string

```

## See Also

[&lc](lc.md); [&replace](replace.md); [&replaceAt](replaceAt.md); [&strrep](strrep.md); [&uc](uc.md)
