colorMenu

Generate a Java Menu color selection component to set accent colors within Cobalt Strike's data model

#### Arguments

`$1` - the prefix

`$2` - an array of IDs to change colors for

#### Example

```
popup targets {
   menu "&Color" {
      insert_color_menu(colorMenu("targets", $1));
   }
}```

See also&highlight
