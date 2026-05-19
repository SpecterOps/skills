listener_pivot_create

Create a new pivot listener.

#### Arguments

`$1` - the Beacon ID

`$2` - the listener name. Valid characters are alphabetic (a-z and A-Z), numeric (0-9), dash (-), period (.), and underscore (_). The name cannot start or end with a period (.).

`$3` - the payload (e.g., windows/beacon_reverse_tcp)

`$4` - the listener host

`$5` - the listener port

#### Note

The only valid payload argument is **windows/beacon_reverse_tcp**.

#### Example

```
# create a pivot listener: 
# $1 = beaconID, $2 = name, $3 = port
alias plisten {
   local('$lhost $bid $name $port');
   
   # extract our arguments
   ($bid, $name, $port) = @_;
   
   # get the name of our target
   $lhost = beacon_info($1, "computer");
   
   btask($1, "create TCP listener on $lhost $+ : $+ $port");
   listener_pivot_create($1, $name, "windows/beacon_reverse_tcp", $lhost, $port);
}```

