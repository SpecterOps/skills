bind

Bind a keyboard shortcut to an Aggressor Script function. This is an alternate to the `bind` keyword.

#### Arguments

`$1` - the keyboard shortcut

`$2` - a callback function. Called when the event happens.

#### Example

```
# bind Ctrl+Left and Ctrl+Right to cycle through previous and next tab.

bind("Ctrl+Left", {
   previousTab();
});

bind("Ctrl+Right", {
   nextTab();
});```

See also&unbind

