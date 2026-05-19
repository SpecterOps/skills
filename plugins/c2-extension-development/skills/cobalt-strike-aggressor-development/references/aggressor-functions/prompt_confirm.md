prompt_confirm

Show a dialog with Yes/No buttons. If the user presses yes, call the specified function.

#### Arguments

`$1` - text in the dialog

`$2` - title of the dialog

`$3` - a callback function. Called when the user presses yes.

#### Example

```
prompt_confirm("Do you feel lucky?", "Do you?", {
   show_mesage("Ok, I got nothing");
});```
