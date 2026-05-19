drow_text

Adds a text field row to a &dialog

#### Arguments

`$1` - a `$dialog` object

`$2` - the name of this row

`$3` - the label for this row

`$4` - (optional) The width of this text field (in characters). This value isn't always honored (it won't shrink the field, but it will make it wider).

#### Example

```
drow_text($dialog, "name", "Name: ");```
