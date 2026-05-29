bpause

Ask Beacon to pause its execution. This is a one-off sleep.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - how long the Beacon should pause execution for (milliseconds)

#### Example

```
alias pause {
   bpause($1, int($2));
}```
