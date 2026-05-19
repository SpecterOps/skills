ssh_command_register

Register help information for an SSH console command.

#### Arguments

`$1` - the command

`$2` - the short description of the command

`$3` - the long-form help for the command.

$4 - (optional) the group id to assign the command. If the group id does not exist, it is ignored.

#### Example

```
ssh_alias echo {
   blog($1, "You typed: " . substr($1, 5));
}

ssh_command_group(
   "ssh_help_group_id",
   "My SSH Help Group Name",
   "This is my example ssh help group");

ssh_command_register(
   "echo", 
   "echo posts to the current session's log", 
   "Synopsis: echo [arguments]\n\nLog arguments to the SSH console");
   "ssh_help_group_id");
```

