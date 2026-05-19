bgetprivs

Attempts to enable the specified privilege in your Beacon session.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - a comma-separated list of privileges to enable. See:

https://msdn.microsoft.com/en-us/library/windows/desktop/bb530716(v=vs.85).aspx

#### Example

```
alias debug {
   bgetprivs($1, "SeDebugPriv");
}```
