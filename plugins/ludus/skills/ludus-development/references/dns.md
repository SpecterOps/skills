# DNS

DNS inside a Ludus range is provided by the user's router, which is running [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome).

AdGuard Home was chosen as it provides the following features important to Ludus:

- DNS rewrites ("pinning")
- DNS blocking/allowing based on requested domain and requesting client
- A REST API

Users can access their AdGuard Home instance at `http://10.{{ range ID }}.{{ any VLAN specified in user's config }}.254:3000`.
The credentials are `admin:password`.

**Note:** Windows VMs, when joined to a domain, will use their primary domain controller for DNS. The domain controller will forward queries outside of its domain to the router.

By default, the AdGuard Home instance includes but does not enable the [Windows Spy](https://github.com/crazy-max/WindowsSpyBlocker) list to block some requests to Microsoft Telemetry.
This blocking is of uncertain value.

## Query Log

The query log shows a log of all DNS queries made to the router VM.

**Note:** If testing mode is not enabled, VMs may make DNS queries to an external DNS server, or use DNS over TLS/HTTPS to resolve domains. These queries will not appear in the Query Log.

## DNS rewrites (pins)

`Filter -> DNS rewrites` show a list of active DNS rewrite rules, or "pins". You can manually edit the rewrites, add your own, or remove existing rewrites.

By default, Ludus adds all VM names, and VM names appended with `home.arpa` to the DNS rewrite list.

## Custom Filtering Rules

`Filters -> Custom rules` shows the active "custom" rules. Ludus uses these rules to enforce testing mode blocks (the `/.*/` rules), and allow rules (the `@@||` rules).

You can learn more about the syntax for these rules [here](https://adguard.com/kb/general/ad-filtering/create-own-filters/).

This is how a range in testing mode with `example.com` allowed looks:
The first two rules block all queries for the two hosts, and the following rules allow example.com and its CRL domains.
