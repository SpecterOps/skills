bsocks

Start a SOCKS proxy server associated with a beacon.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the port to bind to

`$3` - SOCKS version [SOCKS4|SOCKS5] Default: SOCKS4

For SOCKS 5 only:

`$4` - enable/disable NoAuth authentication [enableNoAuth|disableNoAuth] Default: enableNoAuth

`$5` - username for User/Password authentication [blank|username] Default: Blank

`$6` - password for User/Password authentication [blank|password] Default: Blank

`$7` - enable logging [enableLogging|disableLogging] Default: disableLogging

#### Example

```
alias socksPorts {
   bsocks($1, 10401);
   bsocks($1, 10402, "SOCKS4");
   bsocks($1, 10501, "SOCKS5");
   bsocks($1, 10502, "SOCKS5" "enableNoAuth", "", "", "disableLogging");
   bsocks($1, 10503, "SOCKS5" "enableNoAuth", "myname", "mypassword", "disableLogging");
   bsocks($1, 10504, "SOCKS5" "disableNoAuth", "myname", "mypassword", "enableLogging");
}```
