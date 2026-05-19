site_host

Host content on Cobalt Strike's web server

#### Arguments

`$1` - the host for this site (&localip is a good default)

`$2` - the port (e.g., 80)

`$3` - the URI (e.g., /foo)

`$4` - the content to host (as a string)

`$5` - the mime-type (e.g., "text/plain")

`$6` - a description of the content. Shown in **Site Management -> Manage**.

`$7` - use SSL or not (true or false)

#### Returns

The URL to this hosted site

#### Example

```
site_host(localip(), 80, "/", "Hello World!", "text/plain", "Hello World Page", false);```
