bipconfig

Task a Beacon to list network interfaces.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - callback function with the ipconfig results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Example

```
alias ipconfig {
   bipconfig($1, {
      blog($1, "Network information is:\n $+ $2");
   });
}```

