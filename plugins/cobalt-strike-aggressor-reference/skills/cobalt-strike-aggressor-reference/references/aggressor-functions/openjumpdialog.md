openJumpDialog

Open Cobalt Strike's lateral movement dialog

#### Arguments

`$1` - the type of lateral movement. See &beacon_remote_exploits for a list of options. ssh and ssh-key are options too.

`$2` - an array of targets to apply this action against

#### Example

```
openJumpDialog("psexec_psh", @("192.168.1.3", "192.168.1.4"));```

