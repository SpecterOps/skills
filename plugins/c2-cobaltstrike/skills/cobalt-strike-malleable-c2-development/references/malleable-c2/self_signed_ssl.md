# Self-signed SSL Certificats with SSL Beacon

The HTTPS Beacon uses the HTTP Beacon’s indicators in its communication. Malleable C2 profiles may also specify parameters for the Beacon C2 server’s self-signed SSL certificate. This is useful if you want to replicate an actor with unique indicators in their SSL certificate:

```
https-certificate {
     set CN   "bobsmalware.com";
     set O    "Bob’s Malware";
}
```

The certificate parameters under your profile’s control are:

| Option   | Example                 | Description                             |
| -------- | ----------------------- | --------------------------------------- |
| C        | US                      | Country                                 |
| CN       | beacon.cobaltstrike.com | Common Name; Your callback domain       |
| L        | Washington              | Locality                                |
| O        | Fortra, LLC             | Organization Name                       |
| OU       | Certificate Department  | Organizational Unit Name                |
| ST       | DC                      | State or Province                       |
| validity | 365                     | Number of days certificate is valid for |
