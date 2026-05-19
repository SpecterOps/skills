bsleepu

Ask Beacon to change its beaconing interval and jitter factor.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - beacon sleep period string.

The beacon sleep period string takes the format: `ud vh xm ys zj`

Were:

w is the number of days

v is the number of hours

x is the number of minutes

y is the number of seconds

z is the jitter factor [0 - 99]

#### Example

```

            alias stealthy {
   # sleep for 2 days 13 hours 45 minutes 8 seconds with 30% jitter factor
   bsleepu($1, "2d 13h 45m 8s 30j");
}
        ```
