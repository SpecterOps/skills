prompt_directory_open

Show a directory open dialog.

#### Arguments

`$1` - title of the dialog

`$2` - default value

`$3` - true/false: allow user to select multiple folders?

`$4` - a callback function. Called when the user chooses a folder. The argument to the callback is the selected folder. If multiple folders are selected, they will still be specified as the first argument, separated by commas.

#### Example

```
prompt_directory_open("Choose a folder", $null, false, {
   show_message("You chose: $1");
});```

