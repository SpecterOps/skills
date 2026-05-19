bsocks_stop

Stop SOCKS proxy servers associated with the specified Beacon.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
alias stopsocks {
   bsocks_stop($1);
}```

