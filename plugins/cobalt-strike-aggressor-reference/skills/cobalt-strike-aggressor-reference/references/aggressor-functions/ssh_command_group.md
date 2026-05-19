ssh_command_group

Register an SSH Help Group. A Help Group can assist with organizing the SSH console's **help** command output (see SSH console **help help**). Groups will not appear in help until you register commands for the group. Added groups will reset when a client disconnects.

#### Arguments

`$1` - the group id (registers commands to the group). Do not include "," or "@" characters in group ids.

$2 - group name

$3 - group description

#### Example

```
ssh_alis echo {
   blog($1, "You typed: " . substr($1, 5));
}

ssh_command_group(
   "ssh_help_group_id",
   "My SSH Group Name",
   "This is my example ssh help group");

ssh_command_register(
   "echo",
   "echo posts to the current session's log",
   "Synopsis: echo [arguments]\n\nLog arguments to the SSH console",
   "ssh_help_group_id");
```

