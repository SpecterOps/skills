brunasadmin

REMOVED Removed in Cobalt Strike 4.0. Use &belevate_command with psexec_psh option.

Ask Beacon to run a command in a high-integrity context (bypasses UAC).

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the command and its arguments.

#### Notes

This command uses the Token Duplication UAC bypass. This bypass has a few requirements:

- Your user must be a local admin
- If **Always Notify** is enabled, an existing high integrity process must be running in the current desktop session.

#### Example

```
# disable the firewall
brunasadmin($1, "cmd.exe /C netsh advfirewall set allprofiles state off");```

