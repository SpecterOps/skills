prompt_file_open

Show a file open dialog.

#### Arguments

`$1` - title of the dialog

`$2` - default value

`$3` - true/false: allow user to select multiple files?

`$4` - a callback function. Called when the user chooses a file to open. The argument to the callback is the selected file. If multiple files are selected, they will still be specified as the first argument, separated by commas.

#### Example

```
prompt_file_open("Choose a file", $null, false, {
   show_message("You chose: $1");
});```
