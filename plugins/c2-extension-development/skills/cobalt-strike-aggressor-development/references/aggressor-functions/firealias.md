fireAlias

Runs a user-defined alias

#### Arguments

`$1` - the beacon id to run the alias against

`$2` - the alias name to run

`$3` - the arguments to pass to the alias.

#### Example

```
# run the foo alias when a new Beacon comes in
on beacon_initial {
   fireAlias($1, "foo", "bar!");
}```
