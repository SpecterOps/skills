pi_user_explicit_set

Sets the 'Name' for the actively selected user-defined explicit injection. User-defined explicit injections supersede built-in explicit injection selections.

#### Arguments

$1 - Name of the user-defined explicit injection. This injection must have been added to the map of available explicit injections via the PROCESS_INJECT_EXPLICIT_USER hook.

#### Example

```
pi_user_explicit_set("MyFavoriteExplicitInjection-x64");```
