# DNS Beacons

You have the option to shape the DNS Beacon/Listener network traffic with Malleable C2.

```
dns-beacon "optional-variant-name" {
    # Options moved into 'dns-beacon' group in 4.3: 
    set dns_idle              "1.2.3.4";
    set dns_max_txt           "199";
    set dns_sleep             "1";
    set dns_ttl               "5";
    set maxdns                "200";
    set dns_stager_prepend    "doc-stg-prepend"; 
    set dns_stager_subhost    "doc-stg-sh.";

    # DNS subhost override options added in 4.3: 
    set beacon                "doc.bc.";
    set get_A                 "doc.1a.";
    set get_AAAA              "doc.4a.";
    set get_TXT               "doc.tx.";
    set put_metadata          "doc.md.";
    set put_output            "doc.po.";
    set ns_response           "zero";
    set comm_mode	       "dns"; 
}
```

The settings are:

| Option             | Default Value  | Changes                                                                                                                                                                                               |
| ------------------ | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dns_idle           | 0.0.0.0        | IP address used to indicate no tasks are available to DNS Beacon; Mask for other DNS C2 values.                                                                                                       |
| dns_max_txt        | 252            | Maximum length of DNS TXT responses for tasks.                                                                                                                                                        |
| dns_sleep          | 0              | Force a sleep prior to each individual DNS request (in milliseconds).                                                                                                                                 |
| dns_stager_prepend |                | Prepend text to payload stage delivered to DNS TXT record stager.                                                                                                                                     |
| dns_stager_subhost | .stage.123456. | Subdomain used by DNS TXT record stager.                                                                                                                                                              |
| dns_ttl            | 1.             | TTL for DNS replies.                                                                                                                                                                                  |
| maxdns             | 255.           | Maximum length of hostname when uploading data over DNS (0-255).                                                                                                                                      |
| beacon             |                | DNS subhost prefix used for beaconing requests (lowercase text).                                                                                                                                      |
| get_A              | cdn.           | DNS subhost prefix used for A record requests (lowercase text).                                                                                                                                       |
| get_AAAA           | www6.          | DNS subhost prefix used for AAAA record requests (lowercase text).                                                                                                                                    |
| get_TXT            | api.           | DNS subhost prefix used for TXT record requests (lowercase text).                                                                                                                                     |
| put_metadata       | www.           | DNS subhost prefix used for metadata requests (lowercase text).                                                                                                                                       |
| put_output         | post.          | DNS subhost prefix used for output requests (lowercase text).                                                                                                                                         |
| ns_response        | drop           | How to process NS Record requests. `"drop"` does not respond to the request (default), `"idle"` responds with A record for IP address from `"dns_idle"`, `"zero"` responds with A record for 0.0.0.0. |
| comm_mode          | dns            | Used to enable DNS Over HTTPS as the default for the variant. Valid values are `"dns"` or `"dns-over-https"`.                                                                                         |

You can use "ns_response" when a DNS server is responding to a target with "Server failure" errors. A public DNS Resolver may be initiating NS record requests that the DNS Server in Cobalt Strike Team Server is dropping by default.

```
{target}      {DNS Resolver} Standard query 0x5e06 A doc.bc.11111111.a.example.com


{DNS Resolver} {target}       Standard query response 0x5e06 Server failure A doc.bc.11111111.a.example.com
```

## dns-over-https

```
dns-beacon "doh_example" {
    set       comm_mode                   "dns-over-https"; 
    dns-over-https {
    	set       doh_verb                "POST";
    	set       doh_useragent           "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)";
    	set       doh_proxy_server        "https://my.proxy.server:99";
    	set       doh_server              "mozilla.cloudflare-dns.com,cloudflare-dns.com";
    	set       doh_accept              "application/dns-message"; 
    	header   "Content-Type"           "application/dns-message";
        header   "Header-2"               "header2";
    }
}
```

The settings are:

| Option           | Default Value                                 | Changes                                                                            |
| ---------------- | --------------------------------------------- | ---------------------------------------------------------------------------------- |
| doh_verb         | POST                                          | Uses `"GET"` or `"POST"` values.                                                   |
| doh_useragent    |                                               | User agent string used when opening an internet connection. Maximum length is 128. |
| doh_proxy_server |                                               | Specifies a proxy server to egress HTTPS.                                          |
| doh_server       | mozilla.cloudflare-dns.com,cloudflare-dns.com | Comma separated list of DOH servers to use. Maximum length is 256.                 |
| doh_accept       | application/dns-message                       | Used as the “accept types” on the open request API. Maximum length is 128.         |
| header           | Content-Type application/dns-message          | Defines headers used to decorate the HTTPS requests.                               |
