dialog

Create a dialog. Use &dialog_show to show it.

#### Arguments

`$1` - the title of the dialog

`$2` - a %dictionary mapping row names to default values

`$3` - a callback function. Called when the user presses a &dbutton_action button. `$1` is a reference to the dialog. `$2` is the button name. `$3` is a dictionary that maps each row's name to its value.

#### Returns

A scalar with a `$dialog` object.

#### Example

```
sub callback {
   # prints: Pressed Go, a is: Apple
   println("Pressed $2 $+ , a is: " . $3['a']);
}

$dialog = dialog("Hello World", %(a => "Apple", b => "Bat"), &callback);
drow_text($dialog, "a", "Fruit:  ");
drow_text($dialog, "b", "Rodent: ");
dbutton_action($dialog, "Go");
dialog_show($dialog);```
