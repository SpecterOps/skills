pref_get

Grabs a string value from Cobalt Strike's preferences.

#### Arguments

`$1` - the preference name

`$2` - the default value [if there is no value for this preference]

#### Returns

A string with the preference value.

#### Example

```
$foo = pref_get("foo.string", "bar");```
