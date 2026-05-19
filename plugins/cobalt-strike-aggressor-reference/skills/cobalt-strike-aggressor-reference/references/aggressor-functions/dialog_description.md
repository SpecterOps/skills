dialog_description

Adds a description to a &dialog

#### Arguments

`$1` - a `$dialog` object

`$2` - the description of this dialog

`$3` - (optional) the number of lines of text to show for the description of this dialog. When it is not specified two lines of text are shown for the description of this dialog. The maximum number of lines that can be shown is 20.

#### Example

```
dialog_description($dialog, "I am the Hello World dialog.");```

```
dialog_description($dialog, "I am the Hello World dialog.", 2);```

