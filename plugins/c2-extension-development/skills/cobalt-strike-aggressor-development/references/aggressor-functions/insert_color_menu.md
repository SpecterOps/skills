insert_color_menu

Add a color selection menu to a menu tree

#### Arguments

`$1` - the color menu component to add

#### Example

```
popup targets {
   menu "&Color" {
      insert_color_menu(colorMenu("targets", $1));
   }
}```

See also&highlight
