btask

Report a task acknowledgement for a Beacon. This task acknowledgement will also contribute to the narrative in Cobalt Strike's Activity Report and Sessions Report.

#### Arguments

`$1` - the id for the beacon to post to

`$2` - the text to post

`$3` - a string with MITRE ATT&CK Tactic IDs. Use a comma and a space to specify multiple IDs in one string.

https://attack.mitre.org

#### Example

```
alias foo {
   btask($1, "User tasked beacon to foo", "T1015");
}```
