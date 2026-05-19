insert_menu

Bring menus associated with a popup hook into the current menu tree.

#### Arguments

`$1` - the popup hook

`...` - additional arguments are passed to the child popup hook.

#### Example

```
popup beacon {
   # menu definitions above this point
   
   insert_menu("beacon_bottom", $1);
   
   # menu definitions below this point
}```
