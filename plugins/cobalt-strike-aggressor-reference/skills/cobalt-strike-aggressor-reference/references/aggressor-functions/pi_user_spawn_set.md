pi_user_spawn_set

Sets the 'Name' for the actively selected user-defined spawn injection. User-defined spawn injections supersede built-in spawn injection selections.

#### Arguments

$1 - Name of the user-defined spawn injection. This injection must have been added to the map of available explicit injections via the PROCESS_INJECT_SPAWN_USER hook.

#### Example

```
pi_user_spawn_set("MyFavoriteSpawnInjection-x64");```

