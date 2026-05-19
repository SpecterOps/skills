bsteal_token

Ask Beacon to steal a token from a process.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the PID to take the token from

```
Use: bsteal_token [pid]
     bsteal_token [pid] <OpenProcessToken access mask>

OpenProcessToken access mask suggested values:
  blank = default (TOKEN_ALL_ACCESS)
      0 = TOKEN_ALL_ACCESS
     11 = TOKEN_ASSIGN_PRIMARY | TOKEN_DUPLICATE | TOKEN_QUERY (1+2+8)

Access mask values:
  STANDARD_RIGHTS_REQUIRED . . . . : 983040
  TOKEN_ASSIGN_PRIMARY . . . . . . : 1
  TOKEN_DUPLICATE  . . . . . . . . : 2
  TOKEN_IMPERSONATE  . . . . . . . : 4
  TOKEN_QUERY  . . . . . . . . . . : 8
  TOKEN_QUERY_SOURCE . . . . . . . : 16
  TOKEN_ADJUST_PRIVILEGES  . . . . : 32
  TOKEN_ADJUST_GROUPS  . . . . . . : 64
  TOKEN_ADJUST_DEFAULT . . . . . . : 128
  TOKEN_ADJUST_SESSIONID . . . . . : 256```



NOTE: 'OpenProcessToken access mask' can be helpful for stealing tokens from processes using 'SYSTEM' user and you have this error: *Could not open process token: {pid} (5)*

You can set your preferred default with '.steal_token_access_mask' in the Malleable C2 global options.

#### Example

```
alias steal_token {
   bsteal_token($1, int($2));
}```
