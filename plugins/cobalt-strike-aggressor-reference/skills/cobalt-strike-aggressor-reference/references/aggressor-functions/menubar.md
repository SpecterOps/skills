menubar

Add a top-level item to the menubar.

#### Arguments

`$1` - the description

`$2` - the popup hook

#### Example

```
popup mythings {
   item "Keep out" {
   }
}

menubar("My &Things", "mythings");```

