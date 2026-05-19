bnet

Run a command from Beacon's network and host enumeration tool.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command to run.

| Description |  |
| --- | --- |
| lists hosts in a domain (groups) |  |
| lists domain controllers |  |
| show the current domain |  |
| list domain controller hosts in a domain (groups) |  |
| lists domain trusts |  |
| lists groups and users in groups |  |
| lists local groups and users in local groups |  |
| lists users logged onto a host |  |
| lists sessions on a host |  |
| lists shares on a host |  |
| lists users and user information |  |
| show time for a host |  |
| lists hosts in a domain (browser service) |  |

`$3` - the target to run this command against or $null

`$4` - the parameter to this command (e.g., a group name)

`$5` - (optional) the PID to inject the network and host enumeration tool into or $null

`$6` - (optional) the architecture of the target PID (x86|x64) or $null

`$7` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

NOTE: The domain command executes a BOF using inline_execute and will not spawn or inject into a process

#### Example 

Spawn a temporary process```
# ladmins [target]
#   find the local admins for a target
alias ladmins {
   bnet($1, "localgroup", $2, "administrators");
}```

Inject into the specified process```
# ladmins [pid] [arch] [target]
#   find the local admins for a target
alias ladmins {
   bnet($1, "localgroup", $4, "administrators", $2, $3);
}```

