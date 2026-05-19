bls

Task a Beacon to list files

#### Variations

```
bls($1, "folder");```

Output the results to the Beacon console.

```
bls($1, "folder", &callback);```

Route results to the specified callback function.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - (optional) the folder to list files for. Use "." for the current folder.

`$3` - (optional) callback function with the ls results. Arguments to the callback are: $1 = beacon ID, $2 = the folder, $3 = results

#### Example

```
on beacon_initial {
   bls($1, ".");
}```
