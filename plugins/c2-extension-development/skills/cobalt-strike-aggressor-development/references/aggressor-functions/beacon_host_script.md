beacon_host_script

Locally host a PowerShell script within Beacon and return a short script that will download and invoke this script. This function is a way to run large scripts when there are constraints on the length of your PowerShell one-liner.

#### Arguments

`$1` - the id of the Beacon to host this script with.

`$2` - the script data to host.

#### Returns

A short PowerShell script to download and evaluate the script when run. How this one-liner is used is up to you!

#### Example

```
alias test {
   local('$script $hosted');
   $script = "2 + 2";
   $hosted = beacon_host_script($1, $script);
   
   binput($1, "powerpick $hosted");
   bpowerpick($1, $hosted);
}```
