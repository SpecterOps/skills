dbutton_action

Adds an action button to a &dialog. When this button is pressed, the dialog closes and its callback is called. You may add multiple buttons to a dialog. Cobalt Strike will line these buttons up in a row and center them at the bottom of the dialog.

#### Arguments

`$1` - the `$dialog` object

`$2` - the button label

#### Example

```
dbutton_action($dialog, "Start");
dbutton_action($dialog, "Stop");```
