# iswm

**Category:** Strings

**Source:** https://sleep.dashnine.org/manual/iswm.html

---

## Synopsis

```sleep
? '*filter*' iswm "string"
```

Determine if the specified wildcard pattern is a match to the string.

## Parameters

`'*filter*'` - a wildcard pattern.
The following table provides a refresher of the wildcard matching meta characters.

Meta characterMeaning
*Matches any zero or more characters (non-greedy*)
**Matches any zero or more characters (greedy*)
?Matches a single character
\Escapes a wildcard character i.e. \*

A greedy matcher will try to consume as many characters as possible before continuing to the next part of the wildcard string.

`"string"` - the string to check

## Examples

**Example:**
```sleep
@strings = @("test", "task", "turf", "tusk", "dusk",
"musk", "tease", "torso", "stochastic");

foreach $var (@strings) {
if ('t*s*' iswm $var) {
println($var);
}
}

```

**Output:**
```
test
task
tusk
tease
torso

```
