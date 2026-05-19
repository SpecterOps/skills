bkerberos_ticket_purge

Ask beacon to purge tickets from the user's kerberos tray

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
alias kerberos_ticket_purge {
   bkerberos_ticket_purge($1);
}```

