beacon_remote_exec_method_register

Register a Beacon remote execute method with Cobalt Strike. This adds an option for use with the **remote-exec** command.

#### Arguments

`$1` - the method short name

`$2` - a description of the method

`$3` - the function that implements the exploit ($1 is the Beacon ID, $2 is the target, $3 is the command+args)

See Also&beacon_remote_exec_method_describe, &beacon_remote_exec_methods, &bremote_exec
