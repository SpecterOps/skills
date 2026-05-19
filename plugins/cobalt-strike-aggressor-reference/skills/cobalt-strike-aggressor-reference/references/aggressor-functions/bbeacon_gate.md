bbeacon_gate

Change the use of beacon gate at runtime to disable/enable the functionality. See Malleable PE, Process Injection, and Post Exploitation > Beacon Gate for more information.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - enable or disable to change the beacon gate behavior.

#### Example

```
# Disable the beacon gate functionality
  bbeacon_gate($1, "disable");```

