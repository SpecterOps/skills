site_kill

Remove a site from Cobalt Strike's web server

#### Arguments

`$1` - the port

`$2` - the URI

#### Example

```
# removes the content bound to / on port 80
site_kill(80, "/");```

