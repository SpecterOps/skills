drow_proxyserver

DEPRECATED This function is deprecated in Cobalt Strike 4.0. The proxy configuration is now tied directly to the listener.

Adds a proxy server field to a &dialog.

#### Arguments

`$1` - a `$dialog` object

`$2` - the name of this row

`$3` - the label for this row

#### Example

```
drow_proxyserver($dialog, "proxy", "Proxy: ");```

