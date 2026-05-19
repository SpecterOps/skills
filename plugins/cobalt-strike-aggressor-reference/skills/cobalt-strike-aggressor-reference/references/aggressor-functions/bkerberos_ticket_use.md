bkerberos_ticket_use

Ask beacon to inject a mimikatz kirbi file into the user's kerberos tray

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the local path the kirbi file

#### Example

```
alias kerberos_ticket_use {
   bkerberos_ticket_use($1, $2);
}```

