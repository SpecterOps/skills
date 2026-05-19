popup_clear

Remove all popup menus associated with the current menu. This is a way to override Cobalt Strike's default popup menu definitions.

#### Arguments

`$1` - the popup hook to clear registered menus for

#### Example

```
popup_clear("help");

popup help {
   item "My stuff!" {
      show_message("This is my menu!");
   }
}```

