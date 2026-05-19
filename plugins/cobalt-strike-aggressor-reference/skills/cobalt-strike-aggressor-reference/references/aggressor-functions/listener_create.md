listener_create

DEPRECATED This function is deprecated in Cobalt Strike 4.0. Use &listener_create_ext

Create a new listener.

#### Arguments

`$1` - the listener name. Valid characters are alphabetic (a-z and A-Z), numeric (0-9), dash (-), period (.), and underscore (_). The name cannot start or end with a period (.).

`$2` - the payload (e.g., windows/beacon_http/reverse_http)

`$3` - the listener host

`$4` - the listener port

`$5` - a comma separated list of addresses for listener to beacon to

#### Example

```
# create a foreign listener
listener_create("My-Metasploit", "windows/foreign_https/reverse_https", 
      "ads.losenolove.com", 443);

# create an HTTP Beacon listener
listener_create("Beacon-HTTP", "windows/beacon_http/reverse_http",
      "www.losenolove.com", 80, 
      "www.losenolove.com, www2.losenolove.com");```

