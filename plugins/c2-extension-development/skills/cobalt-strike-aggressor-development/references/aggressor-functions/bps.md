bps

Task a Beacon to list processes

#### Variations

```
bps($1);```

Output the results to the Beacon console.

```
bps($1, &callback);```

Route results to the specified callback function.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - (optional) callback function with the ps results. Arguments to the callback are: $1 = beacon ID, $2 = results

#### Example

```
on beacon_initial {
   bps($1);
}```



```
alias prepenv {
  btask($1, "Tasked Beacon to find explorer.exe and make it the PPID");
  bps($1, {
    local('$pid $name $entry');
    foreach $entry (split("\n", $2)) {
      ($name, $null, $pid) = split("\\s+", $entry);
      if ($name eq "explorer.exe") {
          bppid($1, $pid);
      }
    }
  });
}```
