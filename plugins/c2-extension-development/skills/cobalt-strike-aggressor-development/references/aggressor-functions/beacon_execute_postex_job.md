beacon_execute_postex_job

Execute a user defined post exploitation task.

#### Arguments

`$1` - the Beacon ID

`$2`- the PID to inject the task or $null for using fork&run

`$3` - a string containing the postex DLL

`$4` - (optional) packed arguments to pass to the postex task

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

`$6` - (optional) the message id type for the postex task. Defaults to CALLBACK_POSTEX_KIT

See Also:*Postex Kit*
