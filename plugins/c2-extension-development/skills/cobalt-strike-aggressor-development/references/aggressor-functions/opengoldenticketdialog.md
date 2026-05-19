openGoldenTicketDialog

open a dialog to help generate a golden ticket

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Golden Ticket" {
   local('$bid');
   foreach $bid ($1) {
      openGoldenTicketDialog($bid);
   }
}```
