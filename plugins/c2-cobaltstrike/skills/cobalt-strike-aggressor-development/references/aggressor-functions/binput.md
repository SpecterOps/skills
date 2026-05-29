binput

Report a command was run to the Beacon console and logs. Scripts that execute commands for the user (e.g., events, popup menus) should use this function to assure operator attribution of automated actions in Beacon's logs.

#### Arguments

`$1` - the id for the beacon to post to

`$2` - the text to post

#### Example

```
# indicate the user ran the ls command
binput($1, "ls");```
