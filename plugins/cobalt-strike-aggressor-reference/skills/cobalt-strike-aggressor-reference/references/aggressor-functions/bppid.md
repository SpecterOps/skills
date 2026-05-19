bppid

Set a parent process for Beacon's child processes

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the parent process ID. Specify 0 to reset to default behavior.

#### Notes

- The current session must have rights to access the specified parent process. 
- Attempts to spawn post-ex jobs under parent processes in another desktop session may fail. This limitation is due to how Beacon launches its "temporary" processes for post-exploitation jobs and injects code into them.

#### Example

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

