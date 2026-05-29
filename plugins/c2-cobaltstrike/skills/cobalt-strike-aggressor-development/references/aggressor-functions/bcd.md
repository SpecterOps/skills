bcd

Ask a Beacon to change it's current working directory.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the folder to change to.

#### Example

```
# create a command to change to the user's home directory
alias home {
   $home = "c:\\users\\" . binfo($1, "user");
   bcd($1, $home);
}```
