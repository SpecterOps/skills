# hasmatch

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/hasmatch.html

---

## Synopsis

```sleep
"string" hasmatch 'pattern'
```

Determine if the string contains a substring that matches the specified pattern. Subsequent calls to this predicate with the same string, pattern combination will check if there is another pattern beyond the first one.

## Parameters

`"string"` - the string to check

`'pattern'` - a regular expression pattern that defines a substring to match for

- [6. Regular Epxressions](regex.md) - tutorial on regular expression language

## Side Effects / Notes

- This predicate stores state! Each check attempts to locate the next matching substring. When the last matching substring is found, false is returned and the checker is reset.

## Examples

**Example:**
```sleep
sub printDocumentTree
{
local('$tag $content');

while ($1 hasmatch '<(.*?)>(.*?)</\1>')
{
($tag, $content) = matched();
println((" " x $2) . "+- $tag $+ : $content");
printDocumentTree($content, $2 + 1);
}
}

$html = "<html><title>Hello World!</title><p>It's a <b>nice</b> day</p></html>";
printDocumentTree($html, 0);

```

**Output:**
```
+- html: <title>Hello World!</title><p>It's a <b>nice</b> day</p>
+- title: Hello World!
+- p: It's a <b>nice</b> day
+- b: nice

```

## See Also

[&find](find.md); [ismatch](ismatch.md); [&join](join.md); [&matched](matched.md); [&matches](matches.md); [&replace](replace.md); [&split](split.md)
