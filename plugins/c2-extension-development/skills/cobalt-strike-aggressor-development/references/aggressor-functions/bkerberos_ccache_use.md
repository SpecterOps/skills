bkerberos_ccache_use

Ask beacon to inject a UNIX kerberos ccache file into the user's kerberos tray

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the local path the ccache file

#### Example

```
alias kerberos_ccache_use {
   bkerberos_ccache_use($1, $2);
}```
