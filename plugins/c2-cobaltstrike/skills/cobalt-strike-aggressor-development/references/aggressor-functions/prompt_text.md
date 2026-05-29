prompt_text

Show a dialog that asks the user for text.

#### Arguments

`$1` - text in the dialog

`$2` - default value in the text field.

`$3` - a callback function. Called when the user presses OK. The first argument to this callback is the text the user provided.

#### Example

```
prompt_text("What is your name?", "Cyber Bob", {
   show_mesage("Hi $1 $+ , nice to meet you!");
});```
