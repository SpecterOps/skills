bsleep

Ask Beacon to change its beaconing interval and jitter factor.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the number of **seconds** between beacons.

`$3` - the jitter factor [0-99]

#### Example

```
alias stealthy {
   # sleep for 1 hour with 30% jitter factor
   bsleep($1, 60 * 60, 30);
}```
