beacon_command_group

Register a Help Group. A Help Group can assist with organizing the Beacon console's **help** command output (see Beacon console **help help**). Groups will not appear in help until you register commands for the group. Added groups will reset when a client disconnects.

#### Arguments

`$1` - the group id (registers commands to the group). Do not include "," or "@" characters in group ids.

$2 - group name

$3 - group description

#### Example

```
alis echo {
   blog($1, "You typed: " . substr($1, 5));
}

beacon_command_group(
   "my_help_group_id",
   "My Help Group Name",
   "This is my example help group");

beacon_command_register(
   "echo",
   "echo text to beacon log",
   "Synopsis: echo [arguments]\n\nLog arguments to the Beacon console",
   "my_help_group_id");
```

