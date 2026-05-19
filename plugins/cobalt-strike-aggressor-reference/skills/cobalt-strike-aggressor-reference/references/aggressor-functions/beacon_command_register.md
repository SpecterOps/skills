beacon_command_register

Register help information for a Beacon command.

#### Arguments

`$1` - the command

`$2` - the short description of the command

`$3` - the long-form help for the command.

$4 - (optional) the group id to assign the command. If the group id does not exist, it is ignored.

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
   "Synopsis: echo [arguments]\n\nLog arguments to the beacon console");
   "my_help_group_id");
```

#### See Also

*User Defined Tab Completion*

